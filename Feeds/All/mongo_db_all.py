#!/usr/bin/env python

import os
import sys

file_path = os.path.abspath(os.path.abspath(__file__))
sys.path.append(file_path)

from GlobalConfigs  import news_collection_cric, news_collection_f1rc, news_collection_bask,\
        news_collection_tenn, news_collection_ftbl, news_collection_ftbl, news_collection_all



class AllFeedMongo(object):

        @staticmethod
        def if_news_exists(news_id, news_link):
                if news_collection_all.find_one({"news_id": news_id, "news_link": news_link}):
                        return True
                
                return False

        
        @staticmethod
        def insert_news(news_dict):
                news_collection_all.insert(news_dict)
                """
                bulk = news_collection_bask.initialize_unordered_bulk_op()
                for news_dict in news_list:
                        bulk.insert(news)
                bulk.execute()
                """
                return
