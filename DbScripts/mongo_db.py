#!/usr/bin/env python

import os
import sys

file_path = os.path.abspath(os.path.abspath(__file__))
sys.path.append(file_path)

from GlobalConfigs  import news_collection_cric, news_collection_f1rc, news_collection_bask,\
        news_collection_tenn, news_collection_ftbl, news_collection_ftbl



class CricFeedMongo(object):

        @staticmethod
        def check_cric(news_id):
                if news_collection_cric.find_one({"news_id": news_id}):
                        return True
                
                return False

        
        @staticmethod
        def insert_news(news):
                news_collection_cric.insert(news)
                return 



class GenericFeedMongo(object):
        pass
