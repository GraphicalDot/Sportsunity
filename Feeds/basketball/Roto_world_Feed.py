#!/usr/bin/env python

import sys
import os
import json
import time
import feedparser
import urllib
from nltk.tokenize import sent_tokenize
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db_basketball import BasketFeedMongo
from GlobalLinks import *
from Feeds.download_image import ImageDownload
class Basketball_Roto:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,Roto_world):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(Roto_world)
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
        for val in self.list_of_fresh_links:
	    response = urllib.urlopen(val)
            headers = response.info()
	    publish_date=time.mktime(time.strptime(headers['date'], "%a, %d %b %Y %H:%M:%S %Z"))
            article = goose_instance.extract(val)
            full_text = article.cleaned_text.format()
            title = article.title
	    tokenized_data=sent_tokenize(full_text)
	    length_tokenized_data=len(tokenized_data)
            
            if length_tokenized_data > 2:
                summary=tokenized_data[0]+tokenized_data[1]+tokenized_data[2]
            elif length_tokenized_data <2:
                summary=tokenized_data[0]
            else:
                summary = article.meta_description

	    image = article.top_image.get_src()

	    if image.endswith(".jpg") or image.endswith(".png")==True:
		obj1=ImageDownload(image)
		all_formats_image=obj1.runn()
	    else:
		all_formats_image={'ldpi':None,'mdpi':None,'hdpi':None}

	    _dict = {"website":"Roto_world", "news_id":val,"publish_date":publish_date,"summary":summary,"news":full_text, "title":title, "image":image,'ldpi':all_formats_image['ldpi'],'mdpi':all_formats_image['mdpi'],'hdpi':all_formats_image['hdpi'],"time_of_storing":time.mktime(time.localtime())}
            BasketFeedMongo.insert_news(_dict)
	BasketFeedMongo.show_news() 

    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """
    
    def checking(self):
    	list_of_fresh_links=list()
        self.list_of_fresh_links = list_of_fresh_links	
        for val in self.list_of_links:
            if not BasketFeedMongo.check_basket(val):
		self.list_of_fresh_links.append(val)
	self.full_news()

    def reflect_data(self):
	return json.dumps(BasketFeedMongo.show_news())

    def run(self):
	self.rss_feeds(Roto_world)
	self.checking()
	return self.reflect_data()


if __name__ == '__main__':
    obj = Basketball_Roto()
    obj.run()
    #obj.rss_feeds(Roto_world)
    #obj.checking()
    #obj.full_news()








