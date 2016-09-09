#!/usr/bin/env python
import calendar
import json
import signal
import sys
import time
import pymongo
from Elasticsearch_1 import elasticsearch_db
from Feeds.amazon_s3 import AmazonS3
from operator import itemgetter
from blessings import Terminal
import connection
from GlobalConfigs import MONGO_SPORTS_UNITY_NEWS_DB, MONGO_SPORTS_UNITY_NEWS_ALL_COLL, MONGO_SPORTS_UNITY_NEWS_CURATED_COLL
import settings
import tornado
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.log import enable_pretty_logging
from tornado.web import asynchronous, MissingArgumentError
from dateutil.parser import parse
from datetime import datetime

terminal = Terminal()


"""
http://localhost:8000/mixed?&image_size=hdpi&limit=10&type_1=cricket
http://localhost:8000/mixed?image_size=hdpi&limit=10&timestamp=1447739320&direction=up

"""

MONGO_CONNECTION  = connection.get_mongo_connection()
collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_ALL_COLL]

try:
    collection.index_information()["type_1"]
    print terminal.on_blue("INdex on type exists")
except Exception as e:
    collection.create_index("type")

try:
    collection.index_information()["publish_epoch_1"]
    collection.drop_index("publish_epoch_1")
except Exception as e:
    collection.create_index([('publish_epoch', pymongo.DESCENDING)])
    print terminal.on_blue("INdex on publish epoch created")


class NewsApiTornado(tornado.web.RequestHandler):
    """
    Api to handle news feed.
    """

    def initialize(self):
        self.collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_ALL_COLL]
        self.set_status(200)

    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        self.limit = int(self.get_argument('limit', 10))
        self.skip = int(self.get_argument('skip', 0))
        self.image_size = self.get_argument('image_size', None)
        self.timestamp = self.get_argument("timestamp", None)
        self.direction = self.get_argument("direction", None)
        self.search = self.get_argument("search", None)
        self.type_1 = self.get_arguments("type_1", strip=True)
        self.success = {"error": False, "success": True, "result": None}
        self.error = {"error": True, "success": False, "messege": None, "status": None}
        self.news_id = self.get_argument("news_id", None)
        self.curated = self.get_argument("curated", None)
        curated_articles_collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_CURATED_COLL]

        if self.image_size not in ["ldpi", "mdpi", "hdpi", "xhdpi"]:
            self.clear()
            self.set_status(400)
            self.error.update({"message": 'Bad Request: Invalid Image size!', "status": 400})
            self.write(self.error)
            self.finish()
            return

        if self.news_id:
            try:
                result = self.collection.find_one({"news_id": self.news_id}, {'_id': False})
                if not result:
                    result = curated_articles_collection.find_one({'news_id': str(self.news_id)}, {'_id': False})
                result["image_link"] = result.pop(self.image_size, '')
                self.success.update({"result": result})
                self.write(self.success)
            except Exception, e:
                print terminal.on_red(str(e))
                self.error.update({"message": str(e), "status": 400})
                self.write(self.error)
            return

        if not self.search:
            query = {}
            curated_query = {}
            published_query = {}
            if self.type_1:
                query.update({'type':{'$in':self.type_1}})
                curated_query.update({'sport_type':{'$in':self.type_1}})
                published_query.update({'sport_type':{'$in':self.type_1}})
                # print query

            if self.timestamp and self.direction:
                self.get_direction(query)
                self.get_direction(curated_query)
                self.get_direction(published_query)
                """
                print self.direction, self.timestamp
                query.update({'publish_epoch':{"$gt": int(self.timestamp)}}) if self.direction == "up" else \
                    query.update({'publish_epoch':{"$lt": int(self.timestamp)}})
                print query
                """

            # if self.curated == "False":
            #     query.update({'news_type': {'$in': ['other', 'blog']}})
            # print query

            try:
                news = list(self.collection.find(query, {'_id': False}).sort('publish_epoch',-1).limit(self.limit).skip(self.skip))

                if self.curated == 'true':
                    published_query.update({'article_type': 'published'})
                    published_curated_news = list(curated_articles_collection.find(published_query, {'_id': False}).sort('publish_epoch',-1).limit(self.limit))
                    news.extend(published_curated_news)

                news_list = self.pop_image(news)

                curated_query.update({'article_type': 'carousel'})
                carousel_result = curated_articles_collection.find(curated_query, {'_id': False}).sort('priority').limit(3)
                carousel_list = self.pop_image(list(carousel_result))

                self.write({"error": False,
                            "success": True,
                            "result": news_list,
                            "carousel": carousel_list
                            })

            except Exception as e:
                print terminal.on_red(str(e))
                self.set_status(500)
                self.write({'message': str(e), 'error': True, 'success': False})

        if self.search:
            result = elasticsearch_db.ElasticSearchApis.do_query(image_size=self.image_size, text_to_search=self.search,
                                    skip=self.skip, limit=self.limit, timestamp=int(self.timestamp) if self.timestamp else None,
                                    direction=self.direction, type_1=self.type_1 if self.type_1 else ['cricket','football'])
            for post in list(result):
                post['image_link'] = post.pop(self.image_size)
            result = sorted(result, key=itemgetter('publish_epoch'),reverse=True)
            result = result[self.skip:]

            ##Instead of using a loop to find image link for image siz, get documents from source form elasticsearch
            self.write({"error": False, "success": True, "result":result})

        self.finish()
        return

    def pop_image(self, list_of_articles):
        article_list = list()
        for post in list_of_articles:
            post["image_link"] = post.pop(self.image_size, '')
            article_list.append(post)
        return article_list

    def get_direction(self, query):
        query.update({'publish_epoch':{"$gt": int(self.timestamp)}}) if self.direction == "up" else \
                query.update({'publish_epoch':{"$lt": int(self.timestamp)}})
        return
        
        @asynchronous
        @tornado.gen.coroutine
        def post(self):
                data = json.loads(self.request.body)
                print data.prettify()


class PublishCuratedArticleTornado(tornado.web.RequestHandler):
    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        response = {}
        try:
            collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_CURATED_COLL]
            self.article_id = self.get_argument('article_id')
            self.article_group_name = str(self.get_argument('article_group_name'))
            self.headline = str(self.get_argument('article_headline'))
            self.article_image = str(self.get_argument('article_image'))
            self.sport_type = str(self.get_argument('article_sport_type'))
            self.content = str(self.get_argument('article_content'))
            self.publish_date = str(self.get_argument('article_publish_date'))
            self.article_type = str(self.get_argument('type'))
            self.poll_question = str(self.get_argument('article_poll_question'))
            self.notification_content = str(self.get_argument('article_notification_content'))

            date = parse(self.publish_date)
            datetime_tuple = datetime.timetuple(date)
            publish_epoch = int(calendar.timegm(datetime_tuple))
            sport_type = 'cricket' if self.sport_type == 'c' else 'football'
            time_of_storing = int(time.mktime(time.localtime()))

            try:
                all_format_images = AmazonS3(self.article_image, self.article_id).run()
            except Exception, e:
                print e
                all_format_images = {"mdpi": None,
                                     "ldpi": None,
                                     "hdpi": None,
                                     "xhdpi": None}

            projection = {'website': 'https://www.sportsunity.co/', 'title': self.headline,
                          'image_link': self.article_image, 'news_link': 'https://www.sportsunity.co/', 'sport_type': sport_type,
                          'summary': self.content, 'published': self.publish_date, 'publish_epoch': publish_epoch,
                          'news_type': 'curated', 'article_type': self.article_type, 'question': self.poll_question,
                          'notification_content': self.notification_content, 'news_id': str(self.article_id), 'month': int(date.month),
                          'day': int(date.day), 'year': int(date.year), 'gmt_epoch': publish_epoch, 'news': self.content,
                          'favicon': 'http://resized.player.images.s3.amazonaws.com/favicon.png', 'custom_summary': self.content,
                          'time_of_storing': time_of_storing, 'mdpi': all_format_images['mdpi'], 'ldpi': all_format_images['ldpi'],
                          'hdpi': all_format_images['hdpi'], 'xhdpi': all_format_images['xhdpi'], 'group_name': self.article_group_name}

            collection.update({'news_id': str(self.article_id)}, {'$set': projection}, upsert=True)
            response.update({'status': settings.STATUS_200, 'info': 'Success'})
        except MissingArgumentError, status:
            response.update({'status': settings.ERROR_400, 'info': status.log_message})
        except Exception, e:
            response.update({'status': settings.ERROR_500, 'info': str(e)})
        finally:
            self.write(response)


class PostCarouselArticleTornado(tornado.web.RequestHandler):
    @asynchronous
    @tornado.gen.coroutine
    def post(self):
        response = {}
        try:
            collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_CURATED_COLL]
            body = json.loads(self.request.body)
            articles = body.get('articles')
            article_type = str(body.get('type'))

            collection.update({'article_type': 'carousel'}, {'$unset': {'priority': ""}, '$set': {'article_type': 'published'}}, False, True)
            collection.update({'article_type': 'carousel'}, {'$set': {'article_type': 'published'}}, False, True)

            if articles:
                for priority, article_id in articles.items():
                    collection.update({'news_id': str(article_id)}, {'$set': {'priority': str(priority),
                                                                              'article_type': article_type}}, upsert=True)

            response.update({'status': settings.STATUS_200, 'info': 'Success'})
        except Exception, e:
            response.update({'status': settings.ERROR_500, 'info': str(e)})
        finally:
            self.write(response)


app = tornado.web.Application([
    (r"/mixed", NewsApiTornado),
    (r"/publish_article", PublishCuratedArticleTornado),
    (r"/post_carousel_article", PostCarouselArticleTornado),
])


def on_shutdown():
    print terminal.red(terminal.bold('Shutting down'))
    tornado.ioloop.IOLoop.instance().stop()

    ##gracefully closing mongo connection
    MONGO_CONNECTION.close()


def main():
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind("8000")
    enable_pretty_logging()
    http_server.start(30)
    loop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
    loop.start()


if __name__ == '__main__':
    print 'Server Reloaded'
    main()
