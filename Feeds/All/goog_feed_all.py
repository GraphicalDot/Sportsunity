#!/usr/bin/env python
"""
Author: kaali
Purpose: Scraps the links from the link 
http://feeds.feedburner.com/NDTV-Cricket
        

Usage:
        instance = EspnCricketRss(scrape_links=True)
        print instance.news
"""

import os
import sys
import time
import feedparser
from BeautifulSoup import BeautifulSoup
import hashlib
from goose import Goose
import random

parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)

from Links import GOOG_ALL_FEED 



class GoogAllRss(object):
        
        def __init__(self):
                self.all_countries = ["au", "en_ie", "pk", "pl", "uk", "en_za", "en_zw"]
                self.goose_instance = Goose()
                for country in self.all_countries:
                        link =  GOOG_ALL_FEED.replace("country_name", country)
                        self.__each_country(link)


        def __each_country(self, link):
                rss = feedparser.parse(link)
                news_entries = rss["entries"]
                base_link = rss["href"]
                
                self.__rss(news_entries, base_link)
                



        def __rss(self, news_entries, base_link):
                news_list = list()

                for news in news_entries:
                        time.sleep(random.choice(range(10)))
                        soup = BeautifulSoup(news["summary"]) 
                        text = soup.getText()

                        full_text = self.__full_text(self.goose_instance, news["link"])
                        __dict = {"link": news["link"],
                                "published": news["published"],
                                "published_parsed": news["published_parsed"], 
                                "text": text, 
                                "title": news["title"],
                                "news_id": hashlib.md5(news["link"]).hexdigest(),
                                "images": self.image,
                                "full_text": full_text,
                                "base_link": base_link, 
                                "website": "GOOGLE", 
                                }
                        print __dict
                        news_list.append(__dict)



        def __full_text(self, goose_instance, link):
                article = goose_instance.extract(link)
                try:
                        image = article.top_image
                        self.image = image.get_src()
                except :
                        self.image = None
                
                return article.cleaned_text
                

if __name__ == "__main__":
        instance = GoogAllRss()
        
