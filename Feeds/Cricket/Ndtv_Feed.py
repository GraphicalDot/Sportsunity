#!/usr/bin/env python

import sys
import os
import time
import json
import feedparser
import urllib
from nltk.tokenize import sent_tokenize
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db import CricFeedMongo
from GlobalLinks import *
#from Links import NDTV_CRICKET_FEED
#from dbdb_mongo import Data_Management 
class Cricket_NDTV:
    
    """
    This function gets the links of all
    the news articles on the Rss feed and
    stores them in list_of_links
    """

    def rss_feeds(self,NDTV_CRICKET_FEED):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(NDTV_CRICKET_FEED)
        self.details = self.d.entries
        for entry in self.details:
            self.list_of_links.append(entry['id'])
            #self.news_id = entry.id
            
        print self.list_of_links

    """
    This function gets the full text from all
    the links in the list_of_links, only after checking
    for redundancy
    """

    def full_news(self):
        goose_instance = Goose()
        for val in self.list_of_links:
	    response = urllib.urlopen(val)
	    headers = response.info()
	    publish_date=time.mktime(time.strptime(headers['date'], "%a, %d %b %Y %H:%M:%S %Z"))
            article = goose_instance.extract(val)
            full_text = article.cleaned_text.format()
            title = article.title
	    tokenized_data = sent_tokenize(full_text)
	    if tokenized_data[2]:
		summary=tokenized_data[0]+tokenized_data[1]+tokenized_data[2]
	    else:
		summary=article.meta_description
	    #summary = article.meta_description
	    image = article.top_image.get_src()
	    _dict = {"website":"NDTV_CRICKET_FEED","news_id":val,"summary":summary,"publish_date":publish_date,"news":full_text,"title":title,"image":image,"time_of_storing":time.mktime(time.localtime())}
            CricFeedMongo.insert_news(_dict)
        CricFeedMongo.show_news()


    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """

    def checking(self):
        for val in self.list_of_links:
            if not CricFeedMongo.check_cric(val):
                self.full_news()

    """
    This function is used in the API to
    reflect the data from the database.
    """
    
    def reflect_data(self):
	return json.dumps(CricFeedMongo.show_news())


    def run(self):
	self.rss_feeds(NDTV_CRICKET_FEED)
	self.checking()
        return self.reflect_data()


if __name__ == '__main__':
    obj = Cricket_NDTV()
    obj.run()
    #obj.rss_feeds(NDTV_CRICKET_FEED)
    #obj.checking()
    #obj.full_news()





