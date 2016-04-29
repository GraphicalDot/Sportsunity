#!/usr/bin/env python
#*--encoding: utf-8 --*


import sys
import unittest
import requests
import pymongo
import json


conn = pymongo.MongoClient()
db = conn.SPORTS_UNITY_NEWS
SPORTS_UNITY_NEWS_ALL = db.SPORTS_UNITY_NEWS_ALL

class NewsTestCases(unittest.TestCase):

    def test_sport_type(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=ldpi&type_1=football')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article in data['result']:
            article_info = SPORTS_UNITY_NEWS_ALL.find_one({'news_id':article['news_id']})
            self.assertEqual(article_info['sport_type'],'football')           

    def test_publish_epoch_greater(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=ldpi&timestamp=1455848162&direction=up')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article in data['result']:
            assert int(article['publish_epoch']) > 1455848162

    def test_publish_epoch_lesser_and_sport_type(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=ldpi&type_1=football&timestamp=1455848162&direction=down')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article in data['result']:
            article_info = SPORTS_UNITY_NEWS_ALL.find_one({'news_id':article['news_id']})
            self.assertEqual(article_info['sport_type'],'football')
            assert int(article['publish_epoch']) < 1455848162 

    def test_search_celebrity(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=ldpi&search=Virat kohli&type_1=cricket')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article in data['result']:
            article_info = SPORTS_UNITY_NEWS_ALL.find_one({'news_id':article['news_id']})
            option1 = 'virat kohli'
            option2 = 'Kohli'
            #self.assertIn(option2,article_info['news'])
            assert (option1 in article_info['news'] or option2 in article_info['news'])

    def test_image_size(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=hdpi&type_1=football&timestamp=1455848162&direction=down')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article in data['result']:
            assert ('image_link' in article.keys() and article['image_link'].endswith('hdpi.png'))

    def test_if_correct_news_id(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=hdpi&news_id=1f6b0c99f80710591c6866c36817bff9')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['result']['news_id'],'1f6b0c99f80710591c6866c36817bff9')

    def test_if_news_text_exists(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=20&image_size=mdpi')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        self.assertEqual(len(data['result']),20)
        for article in data['result']:
            article_info = SPORTS_UNITY_NEWS_ALL.find_one({'news_id':article['news_id']})
            self.assertIsNotNone(article_info['news'])

    def test_if_sorted(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=20&image_size=mdpi')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article,next_article in zip(data['result'],data['result'][1:]):
            assert article['publish_epoch']>=next_article['publish_epoch']

    def test_sorted_after_search(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=20&image_size=mdpi&search=kohi&type_1=cricket')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        for article,next_article in zip(data['result'],data['result'][1:]):
            assert article['publish_epoch']>=next_article['publish_epoch']

    def test_news_refresh(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=20&image_size=mdpi')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        timestamp = data['result'][0]['publish_epoch']
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=mdpi&timestamp={}&direction=up'.format(int(timestamp)))
        data = json.loads(res.content)
        assert data['result'] == []

    def test_news_refresh_with_search(self):
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=mdpi&search=kohli&type_1=cricket')
        data = json.loads(res.content)
        self.assertEqual(res.status_code,200)
        timestamp = data['result'][0]['publish_epoch']
        res = requests.get('http://localhost:8000/mixed?skip=0&limit=10&image_size=mdpi&search=kohli&type_1=cricket&timestamp={}&direction=up'.format(int(timestamp)))
        data = json.loads(res.content)
        print data['result']
        assert data['result'] == []



if __name__=='__main__':
    unittest.main()

            




