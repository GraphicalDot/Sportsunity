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
                news_list = self.__filter()

                for news in news_list:
                        time.sleep(random.choice(range(10)))

                        full_text = self.__full_text(self.goose_instance, news["link"])
                    
                        news.pop("scraped")
                        news.update({"images": self.image})
                        news.update({"full_text": full_text})
                         
                        print full_text
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
                        news_id = hashlib.md5(news["link"]).hexdigest(),
                        news_list.append({"link": news["link"],
                                        "published": news["published"],
                                        "epoch": time.mktime(time.strptime(news["published"], "%a, %d %b %Y %H:%M:%S +0000")),
                                        "text": text,
                                        "title": news["title"],
                                        "news_id": news_id,
                                        "scraped": CricFeedMongo.check_cric(news_id),
                                        "base_link": self.base_link,
                                        "website": "CRICBUZZ", 
                                        })

                return filter(lambda x: not x["scraped"], news_list)



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
        
