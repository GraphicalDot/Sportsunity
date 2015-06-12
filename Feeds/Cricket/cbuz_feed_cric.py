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

from Links import CBUZ_CRIC_FEED 



class CbuzCricketRss(object):
        def __init__(self, scrape_links= False, scrape_images=False):
                self.scrape_links = scrape_links
                self.scrape_images = scrape_images

                self.goose_instance = Goose()
                self.rss = feedparser.parse(CBUZ_CRIC_FEED)
                self.news_entries = self.rss["entries"]
                self.base_link = self.rss["href"]
                self.news = list()
                self.__rss()
    



        def __rss(self):
                for news in self.news_entries:
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
                            "base_link": self.base_link, 
                            "website": "CRICBUZZ", 
                            }
                    print __dict
                    self.news.append(__dict)



        def __full_text(self, goose_instance, link):
                if self.scrape_links:
                        article = goose_instance.extract(link)
                        try:
                                image = article.top_image
                                self.image = image.get_src()
                        except :
                                self.image = None
                        return article.cleaned_text
                self.image = None
                return None


if __name__ == "__main__":
        instance = CbuzCricketRss(scrape_links=True)
        print instance.news
        
