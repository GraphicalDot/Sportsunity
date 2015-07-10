#!/usr/bin/env python

import os
import sys

file_path = os.path.abspath(os.path.abspath(__file__))
sys.path.append(file_path)

from GlobalConfigs  import news_collection_cric, news_collection_f1rc, news_collection_bask,\
        news_collection_tenn, news_collection_ftbl, news_collection_all



class Formula1FeedMongo(object):

        @staticmethod
        def check_f1(news_id):
                if news_collection_f1rc.find_one({"news_id": news_id}):
                        return True
                
                return False

        
        @staticmethod
        def insert_news(news):
                news_collection_f1rc.insert(news)
                return

	@staticmethod
	def show_news():
		return list(news_collection_f1rc.find(fields={'_id':False}).sort("publish_date",-1))

	@staticmethod
	def recent_news(args,kwargs):
		if kwargs == "ldpi":
                    return list(news_collection_f1rc.find(fields={'mdpi':False,'hdpi':False,'_id':False}).sort("publish_date",1).skip(0).limit(args))
                elif kwargs == "mdpi":
                    return list(news_collection_f1rc.find(fields={'ldpi':False,'hdpi':False,'_id':False}).sort("publish_date",1).skip(0).limit(args))
                elif kwargs == "hdpi":
                    return list(news_collection_f1rc.find(fields={'ldpi':False,'mdpi':False,'_id':False}).sort("publish_date",1).skip(0).limit(args))
                else:
                    return "Image format not received"	

	@staticmethod
	def number_of_news(args):
		return list(news_collection_f1rc.find(fields={'_id':False}).sort("publish_date",1).limit(args))

	@staticmethod
	def news_in_between(args,kwargs):
		return list(news_collection_f1rc.find({'publish_date': {'$gte':args , '$lt':kwargs}},{'_id':False}).sort('publish_date',1))



class GenericFeedMongo(object):
        pass
