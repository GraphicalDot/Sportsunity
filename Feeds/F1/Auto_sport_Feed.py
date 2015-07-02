#!/usr/bin/env python

import sys
import os
import time
import json
import feedparser
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db_F1 import Formula1FeedMongo
from GlobalLinks import *
#from Links_Formula1 import Auto_sport
class Formula_one_Auto:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,Auto_sport):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(Auto_sport)
        self.details = self.d.entries
        for entry in self.details:
            self.list_of_links.append(entry['link'])
            self.publish = entry['published']
        print self.list_of_links
    
    """
    This function gets the full text from all 
    the links in the list_of_links, only after checking
    for redundancy
    """

    def full_news(self):
        goose_instance = Goose()
        for val in self.list_of_links:
            article = goose_instance.extract(val)
            full_text = article.cleaned_text.format()
            title = article.title
            _dict = {"website":"Auto_sport", "news_id":val, "news":full_text, "title":title, "time_of_Storing":time.mktime(time.localtime())}
            Formula1FeedMongo.insert_news(_dict)
        Formula1FeedMongo.show_news()
    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """
    
    def checking(self):
        for val in self.list_of_links:
            if not Formula1FeedMongo.check_f1(val):
                self.full_news()

    """
    This function is used in the API to
    reflect the data from the database.
    """

    def reflect_data(self):
        return json.dumps(Formula1FeedMongo.show_news())


    def run(self):
        self.rss_feeds(Auto_sport)
        self.checking()
        self.reflect_data()




if __name__ == '__main__':
    obj = Formula_one_Auto()
    obj.run()
    #obj.rss_feeds(Auto_sport)
    #obj.checking()
    #obj.full_news()





