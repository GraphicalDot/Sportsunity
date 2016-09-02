#!/usr/bin/env python
#*--encoding: utf-8 --*

import json
import os
import pymongo
import requests
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import connection
import settings
from GlobalConfigs import MONGO_SPORTS_UNITY_NEWS_DB, MONGO_SPORTS_UNITY_NEWS_CURATED_COLL, MONGO_SPORTS_UNITY_NEWS_ALL_COLL

TORNADO_SERVER = "http://localhost:8000"
MONGO_CONNECTION  = pymongo.MongoClient()
news_db = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB]
news_collection = news_db[MONGO_SPORTS_UNITY_NEWS_ALL_COLL]
curated_articles_collection = news_db[MONGO_SPORTS_UNITY_NEWS_CURATED_COLL]



class PublishCuratedArticleTornadoTests(unittest.TestCase):

    def setUp(self):
        self.publish_curated_article_url = TORNADO_SERVER + '/publish_article'
        self.data = {}

    def test_get(self):
        response = requests.get(self.publish_curated_article_url + '?article_id=100')
        self.assertEqual(response.status_code, settings.ERROR_405)

    def test_post(self):

        # Missing GET data
        response = requests.post(self.publish_curated_article_url)
        res = json.loads(response.text)
        self.assertEqual(res['status'], settings.ERROR_400)
        self.assertEqual(res['info'], 'Missing argument article_id')

        # valid GET data
        self.data = {'article_id': '1367', 'article_headline': 'article_1', 'article_image': 'text',
                     'article_sport_type': 'c', 'article_content': 'text', 'article_publish_date': '31/08/2016',
                     'type': 'published', 'article_poll_question': 'text', 'article_notification_content': 'text'}
        response = requests.post(self.publish_curated_article_url, self.data)
        res = json.loads(response.text)
        self.assertEqual(res['status'], settings.STATUS_200)
        self.assertEqual(res['info'], 'Success')

        result = list(curated_articles_collection.find({'news_id': self.data['article_id']}, {'_id': False}))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], self.data['article_headline'])
        curated_articles_collection.remove({'news_id': self.data['article_id']})


class PostCarouselArticleTornadoTests(unittest.TestCase):

    def setUp(self):
        self.post_carousel_articles_url = TORNADO_SERVER + '/post_carousel_article'

    def test_get(self):
        response = requests.get(self.post_carousel_articles_url)
        self.assertEqual(response.status_code, settings.ERROR_405)

    def test_post(self):
        self.data = {'article_id': '1367', 'article_headline': 'article_1', 'article_image': 'text',
                     'article_sport_type': 'c', 'article_content': 'text', 'article_publish_date': '31/08/2016',
                     'type': 'published', 'article_poll_question': 'text', 'article_notification_content': 'text'}
        requests.post(TORNADO_SERVER + '/publish_article', self.data)

        self.data = json.dumps({'articles': {'100': self.data['article_id']}, 'type': 'carousel'})
        response = requests.post(self.post_carousel_articles_url, self.data)
        res = json.loads(response.text)
        self.assertEqual(res['status'], settings.STATUS_200)
        self.assertEqual(res['info'], 'Success')
        result = list(curated_articles_collection.find({'news_id': '1367'}, {'_id': False}))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['priority'], '100')
        self.assertEqual(result[0]['article_type'], 'carousel')
        curated_articles_collection.remove({'news_id': '1367'})


class NewsApiTornadoForCuratedArticlesTests(unittest.TestCase):

    def setUp(self):
        self.get_news_url = TORNADO_SERVER + '/mixed'
        self.news_articles = {'title': 'news_article_1', 'type': 'cricket', 'summary': 'TEXT', 'publish_epoch': 1444710213,
                               'news_id': 'sssuwsbbiws', 'published': '4/06/2017', 'news_type': 'blog'}
        news_collection.insert(self.news_articles)

        self.curated_articles = [{'title': 'article_1', 'article_type': 'published', 'sport_type': 'cricket', 'news': 'TEXT',
                                  'publish_epoch': 1472601600, 'question': 'text', 'news_id': '1367', 'published': '31/08/2016',
                                  'news_type': 'curated'},
                                 {'title': 'article_2', 'article_type': 'carousel', 'sport_type': 'football', 'news': 'TEXT',
                                  'publish_epoch': 1422601610, 'question': 'text', 'news_id': '1368', 'published': '31/09/2016',
                                  'news_type': 'curated', 'priority': '101'},
                                 {'title': 'article_3', 'article_type': 'carousel', 'sport_type': 'cricket', 'news': 'TEXT',
                                  'publish_epoch': 1472601620, 'question': 'text', 'news_id': '1369', 'published': '31/10/2016',
                                  'news_type': 'curated', 'priority': '100'}]
        for article in self.curated_articles:
            curated_articles_collection.insert(article)

    def test_post(self):
        response = requests.post(self.get_news_url)
        self.assertEqual(response.status_code, settings.ERROR_405)

    def test_get(self):

        # sport_type = cricket, without 'curated' query parameter
        response = requests.get(self.get_news_url + '?image_size=hdpi&limit=5&type_1=cricket')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertTrue(set(['news_article_1']).issubset([article['title'] for article in res['result']]))
        self.assertTrue(set(['article_3']).issubset([article['title'] for article in res['carousel']]))

        # sport_type = cricket, with 'curated' query parameter
        response = requests.get(self.get_news_url + '?image_size=hdpi&limit=5&type_1=cricket&curated=true')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertTrue(set(['news_article_1', 'article_1']).issubset([article['title'] for article in res['result']]))
        self.assertTrue(set(['article_3']).issubset([article['title'] for article in res['carousel']]))

        # sport type = football
        response = requests.get(self.get_news_url + '?image_size=hdpi&limit=5&type_1=football')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertTrue(set(['news_article_1', 'article_1', 'article_2', 'article_3']).isdisjoint([article['title'] for article in res['result']]))
        self.assertTrue(set(['article_2']).issubset([article['title'] for article in res['carousel']]))

        # filter on timestamp and direction
        response = requests.get(self.get_news_url + '?image_size=hdpi&limit=5&timestamp=1447739320&direction=up&curated=true')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertTrue(set(['article_1']).issubset([article['title'] for article in res['result']]))
        self.assertTrue(set(['article_3']).issubset([article['title'] for article in res['carousel']]))

        # filter on news_id of curated article
        response = requests.get(self.get_news_url + '?image_size=ldpi&news_id=1368')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertEqual(res['result']['title'], 'article_2')

        # test carousel articles order
        response = requests.get(self.get_news_url + '?image_size=ldpi')
        res = json.loads(response.text)
        self.assertEqual(res['success'], True)
        self.assertEqual([article['title'] for article in res['carousel'] if article['priority'] in ['100', '101']], ['article_3', 'article_2'])

    def tearDown(self):
        news_collection.remove(self.news_articles)
        for article in self.curated_articles:
            curated_articles_collection.remove(article)


if __name__ == '__main__':
    unittest.main()
