#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection
TIME_STAMP = "publish_epoch"


##Source: The fileds which will be returned per article 
SOURCE = ['website', 'title', 'gmt_epoch', 'month', 'news_link', 'custom_summary', 'publish_epoch', \
          'time_of_storing', 'year','news_id', 'summary', 'sport_type', 'day', 'published', 'favicon']



connection = connection.get_mongo_connection()
sports_db = connection.SPORTS_UNITY_NEWS

MONGO_SPORTS_UNITY_NEWS_ALL_COLL = sports_db.SPORTS_UNITY_NEWS_ALL
