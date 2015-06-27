#!/usr/bin/env python

import sys
import os
import time
import feedparser
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
print parent_dir_path
from DbScripts.mongo_db_tennis import TennFeedMongo
from Links_Tennis import BBC_FEED
class Tennis:
    """
    This function gets the links 
    of all the news articles on the
    Rss Feed and stores them in list_of_links.
    """
    def rss_feeds(self,BBC_FEED):
        list_of_links = list()
        self.list_of_links = list_of_links
        self.d = feedparser.parse(BBC_FEED)
        self.details = self.d.entries
        for entry in self.details:
            self.list_of_links.append(entry['id'])
            
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
            _dict = {"website":"BBC_FEED", "news_id":val, "news":full_text, "title":title, "time_of_storing":time.mktime(time.localtime())}
            TennFeedMongo.insert_news(_dict)
    
    """
    This function checks for duplicate news_ids.
    If a duplicate is found function full_news doesn't run
    """
    
    def checking(self):
        for val in self.list_of_links:
            if not TennFeedMongo.check_tenn(val):
                self.full_news()


if __name__ == '__main__':
    obj = Tennis()
    obj.rss_feeds(BBC_FEED)
    obj.checking()
    #obj.full_news()






