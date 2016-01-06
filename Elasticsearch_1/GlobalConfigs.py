#!/usr/bin/env python

import pymongo
TIME_STAMP = "publish_epoch"


##Source: The fileds which will be returned per article 
SOURCE = ['website', 'title', 'gmt_epoch', 'month', 'news_link', 'custom_summary', 'publish_epoch', \
        'time_of_storing', 'year', 'news', 'news_id', 'summary', 'type', 'day', 'published', 'favicon']




connection = pymongo.MongoClient("localhost")
sports_db = connection.admin
sports_db.authenticate('shivam','mama123')
sports_db = connection.SPORTS_UNITY_NEWS


MONGO_SPORTS_UNITY_NEWS_ALL_COLL = sports_db.SPORTS_UNITY_NEWS_ALL
ELASTICSEARCH_IP = "localhost"



