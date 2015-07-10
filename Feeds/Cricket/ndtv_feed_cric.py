#!/usr/bin/env python
"""
Author: kaali
Purpose: Scraps the links from the link 
http://feeds.feedburner.com/NDTV-Cricket
        

Usage:
        instance = NdtvCricketRss(scrape_links=True)
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

from DbScripts.mongo_db import CricFeedMongo
from Links import NDTV_CRICKET_FEED 



class NdtvCricketRss(object):
        def __init__(self, scrape_links= False, scrape_images=False):
                self.scrape_links = scrape_links
                self.scrape_images = scrape_images

                self.goose_instance = Goose()
                self.rss = feedparser.parse(NDTV_CRICKET_FEED)
                self.news_entries = self.rss["entries"]
                self.base_link = self.rss["href"]
                self.news = list()
                self.__rss()
    



        def __rss(self):
                for news in self.news_entries:
                    time.sleep(random.choice(range(10)))
                    soup = BeautifulSoup(news["summary"]) 
                    images =  [img["src"] for img in soup.findAll("img")]
                    text = soup.getText()

                    full_text = self.__full_text(self.goose_instance, news["id"])
                    __dict = {"link": news["id"],
                            "published": news["published"],
                            "published_parsed": news["published_parsed"], 
                            "text": text, 
                            "tags": news["tags"], 
                            "title": news["title"],
                            "news_id": hashlib.md5(news["id"]).hexdigest(),
                            "images": images,
                            "full_text": full_text,
                            "base_link": self.base_link, 
                            "website": "NDTV", 
                            }
                    print __dict
                    CricFeedMongo.insert_news(__dict)
                    self.news.append(__dict)
        def __filter(self):
                """
                Filter rss on the basis if they are prsent in the mongodb or not
                he purpose of checking the enteries in the mongodb is to save the goose
                scraping og the full text
                """
                news_list = list()
                for news in self.news_entries:
                        soup = BeautifulSoup(news["summary"])
                        text = soup.getText()
                        news_id = hashlib.md5(news["id"]).hexdigest(),
                        news_list.append({"link": news["id"],
                                        "published": news["published"],
                                        "epoch": time.mktime(time.strptime(news["published"], "%a, %d %b %Y %H:%M:%S %Z")),
                                        "text": text,
                                        "title": news["title"],
                                        "news_id": news_id,
                                        "scraped": CricFeedMongo.check_cric(news_id),
                                        "base_link": self.base_link,
                                        "website": "BBC",
                                        })

                return filter(lambda x: not x["scraped"], news_list)



        def __full_text(self, goose_instance, link):
                if self.scrape_links:
                        article = goose_instance.extract(link)
                        return article.cleaned_text
                return None


if __name__ == "__main__":
    obj = NdtvCricketRss(object)
    #obj._rss
    #obj._filter
    #obj._full_text
