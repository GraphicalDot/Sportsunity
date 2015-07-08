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
from flask import jsonify
from DbScripts.mongo_db_basketball import BasketFeedMongo
from GlobalLinks import *
#from Links_Basketball import Inside_hoops
class Basketball_Hoops:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,Inside_hoops):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(Inside_hoops)
        self.details = self.d.entries
        for entry in self.details:
            self.list_of_links.append(entry['link'])
            
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
            if tokenized_data[1]:
                summary=tokenized_data[0]+tokenized_data[1]
            else:
                summary = article.meta_description
	    #summary = article.meta_description
	    image = article.top_image.get_src()
	    _dict = {"website":"Inside_hoops", "news_id":val,"summary":summary,"publish_date":publish_date,"news":full_text,"title":title,"image":image, "time_of_storing":time.mktime(time.localtime())}
            BasketFeedMongo.insert_news(_dict)
            #print BasketFeedMongo.show_news()
        #return BasketFeedMongo.show_news()
        #return json.dumps((_dict))
    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """

    def checking(self):
        for val in self.list_of_links:
            if not BasketFeedMongo.check_basket(val):
                self.full_news()

    def reflect_data(self):
        return json.dumps(BasketFeedMongo.show_news())
        

    def run(self):
        self.rss_feeds(Inside_hoops)
        self.checking()
        self.reflect_data()


if __name__ == '__main__':
    obj = Basketball_Hoops()
    obj.run()
    #obj.rss_feeds(Inside_hoops)
    #obj.checking()
    #obj.reflect_data()
    #obj.full_news()








