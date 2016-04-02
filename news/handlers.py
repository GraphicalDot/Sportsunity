import os
import sys
import tornado
import tornado.web
from tornado.web import asynchronous
import tornado.gen
import traceback
from pymongo.errors import PyMongoError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import GlobalConfigs
import settings
from Elasticsearch_1 import elasticsearch_db


class NewsRequestHandler(tornado.web.RequestHandler):
    """
    Main Request Handler for News.
    """
    def initialize(self):
        """
        initializes local variables for instance.
        """
        self.limit = int(self.get_argument('limit', 10))
        self.skip = int(self.get_argument('skip', 0))
        self.image_size = self.get_argument('image_size', None)
        self.projection = { "summary": True, "custom_summary": True, "title": True, "website": True, "news_id": True,
                            "published": True, "publish_epoch": True, "news_link": True, "type": True, "gmt_epoch":True,
                            self.image_size: True, "_id": False, "time_of_storing": True, "favicon":True }

    def data_validation(self):
        """
        validates GET data received.
        """
        if self.image_size not in ["ldpi", "mdpi", "hdpi", "xhdpi"]:
            self.response.update({
                'status': settings.ERROR_400,
                'message': 'Bad Request: Invalid Image size!',
                'error': True,
                'success': False,
            })
        return

    def get_news_with_news_id(self, news_id):
        """
        :return: news with particular news_id if success,
                 error if failure.
        """
        self.projection.update({"news": True})
        try:
            news = self.collection.find({"news_id": news_id}, projection=self.projection).sort("publish_epoch",-1)
            if news:
                result = news[0]
                result['image_link'] = result.pop(self.image_size)
                self.response.update({
                    'status': settings.STATUS_200,
                    'message': 'Success',
                    'result': result,
                    'error': False,
                    'success': True
                })
            else:
                self.response.update({
                    'status': settings.ERROR_404,
                    'message': "Not Found: No News matched the 'news_id'! ",
                    'result': news,
                    'error': False,
                    'success': True
                })
        except PyMongoError as e:
            self.response.update({'status': 404, 'message': "Error: %s" % e, 'result': [], 'error': True, 'success': False})

    def get_news_without_search(self, news_type, timestamp, direction):
        """
        :param news_type: could be either 'cricket' or 'football'
        :param timestamp: 'publish_epoch' for news
        :param direction: could be either 'up' or 'down'
        :return: news without elastic search
        """
        query_condition = {}
        if news_type:
            query_condition['type'] = {'$in': [news_type]}

        if timestamp:
            query_condition['publish_epoch'] = {"$gt": timestamp} if direction == 'up' else {"$lt": timestamp}

        return list(self.collection.find(query_condition, projection=self.projection).sort('publish_epoch',-1). \
                    skip(self.skip).limit(self.limit))


    def get_news_with_search(self, news_type, timestamp, direction):
        """
        :param news_type: could be either 'cricket' or 'football'
        :param timestamp: 'publish_epoch' for news
        :param direction: could be either 'up' or 'down'
        :return: news with elastic search
        """
        result = elasticsearch_db.ElasticSearchApis.do_query(argument=self.image_size, text_to_search=self.get_argument('search'),
                                                             skip=self.skip, limit=self.limit, timestamp=timestamp,
                                                             direction=direction, type_1=news_type)
        result = sorted(result,key=itemgetter('publish_epoch'), reverse=True)
        if not timestamp:
            result = result[self.skip:]
        return result

    def get_result(self):
        """
        :return: news list, filtering on different parameters.
        """
        if self.get_argument('news_id', None):
            self.get_news_with_news_id(self.get_argument('news_id'))
        else:
            self.news_type = self.get_argument('type_1', None)
            self.timestamp = self.get_argument('timestamp', None)
            self.direction = self.get_argument('direction', None)

            result = self.get_news_with_search(self.news_type, self.timestamp, self.direction) \
                if self.get_argument('search', None) else self.get_news_without_search(self.news_type, self.timestamp, self.direction)

            for val in result:
                val['image_link'] = val.pop(self.image_size)

            self.response.update({'status': settings.STATUS_200, 'result': result, 'error': False, 'success': True,
                                  'message': 'Success' if result else 'Not Found: No News found!'})


class GetMixedNews(NewsRequestHandler):
    """
    Returns news of following games:
    1. Cricket
    2. Football

    Filters response on following parameters:
    1. image_size
    2. limit
    3. skip
    4. news_id
    5. type_1
    6. timestamp
    7. direction
    """
    @tornado.gen.coroutine
    @asynchronous
    def get(self, *args, **kwargs):
        print 'inside get of GetFootballNews'
        self.response = {'status': 0, 'error': False, 'success': True, 'message': 'Success', 'result': []}
        try:
            self.collection = GlobalConfigs.news_collection_all
            self.data_validation()
            if self.response['status'] not in settings.ERROR_LIST:
                self.get_result()
        except PyMongoError as e:
            self.response.update({ 'status': settings.ERROR_500, 'error': True, 'success': False, 'message': "Error: %s" % e })
        except Exception as e:
            self.response.update({ 'status': settings.ERROR_500, 'error': True, 'success': False, 'message': "Error: %s" % e })
        finally:
            self.write(self.response)
