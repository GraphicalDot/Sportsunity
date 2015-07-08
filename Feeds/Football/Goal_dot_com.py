#!/usr/bin/env python

import sys
import os
import time
import json
import feedparser
import urllib
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db_football import FootFeedMongo
from GlobalLinks import *
class Football_Goal:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,Goal_dot_com):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(Goal_dot_com)
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
	    summary = article.meta_description
	    image = article.top_image.get_src()
	    _dict = {"website":"Goal_dot_com","news_id":val,"summary":summary,"publish_date":publish_date,"news":full_text,"title":title,"image":image,"time_of_storing":time.mktime(time.localtime())}
            FootFeedMongo.insert_news(_dict)

        FootFeedMongo.show_news()
    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """
    
    def checking(self):
        for val in self.list_of_links:
            if not FootFeedMongo.check_foot(val):
                self.full_news()

    """
    This function is used in the API to
    reflect the data from the database.
    """

    def reflect_data(self):
        return json.dumps(FootFeedMongo.show_news())


    def run(self):
        self.rss_feeds(Goal_dot_com)
        self.checking()
	return self.reflect_data()



if __name__ == '__main__':
    obj = Football_Goal()
    obj.run()
    #obj.rss_feeds(Goal_dot_com)
    #obj.checking()
    #obj.full_news()








