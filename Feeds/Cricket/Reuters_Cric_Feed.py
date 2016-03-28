#!/usr/bin/env python

import sys
import os
import time
import calendar
import json
import feedparser
import urllib
from nltk.tokenize import sent_tokenize, word_tokenize
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)
from mongo_db_cricket import CricFeedMongo
from Feeds.All.mongo_db_all import AllFeedMongo
from GlobalLinks import *
from GlobalMethods import unicode_or_bust
from Feeds.amazon_s3 import AmazonS3
import hashlib
from summarize_news import ShortNews
from dateutil.parser import parse
from datetime import datetime


class CricketReuters:
        """
        This function gets the links of all the news articles on the Rss Feed and stores them in list_of_links.
        """
        def __init__(self, link):
                """
                Args:
                    link: link of the rss feed link
                class variables:
                        self.news_list with each entry like this:
                             {'link': u'http://www.fifa.com/beachsoccerworldcup/news/y=2015/m=7/news=portuguese-party-as-stars-shine-on-and-off-the-pitch-2662475.html',
                                'published': u'Thu, 09 Jul 2015 21:36:00 GMT',
                                'summary': u'<p>A fantastic atmosphere awaited the teams in the Praia da Baia Stadium in Espinho as the FIFA Beach Soccer \
                                        World Cup Portugal 2015 got underway. Around 3,500 fans packed into the stands and they got what they wanted &ndash; \
                                        a Portuguese victory over Japan in the Group A opener.</p>',
                                'tags': [{'label': None, 'scheme': None, 'term': u'Area=Tournament'},
                                      {'label': None, 'scheme': None, 'term': u'Section=Competition'},
                                         {'label': None, 'scheme': None, 'term': u'Kind=News'},
                                        {'label': None,
                                        'scheme': None,
                                        'term': u'Tournament=FIFA Beach Soccer World Cup Portugal 2015'}],
                                    'title': u'Portuguese party as stars shine on and off the pitch'}]
                """
                self.link = link
                self.news_list = []
                self.links_not_present = list()
                self.rss = feedparser.parse(self.link)
                self.news_entries = self.rss.entries
                [self.news_list.append({"news_link": news_entry["link"], "published": news_entry["published"], "summary": \
                        news_entry["summary"], "title": news_entry["title"], "news_id": hashlib.md5(news_entry["link"]).hexdigest()}) \
                        for news_entry in self.news_entries]
                                

        def run(self):
                print "Total number of news link in rss %s"%len(self.news_list)
                self.checking()
                print "Number of news links not stored in the databse %s"%len(self.links_not_present)
                self.full_news()
                return 

        def checking(self):
                for news_dict in self.news_list:
                        if not CricFeedMongo().if_news_exists(news_dict["news_id"], news_dict["news_link"]) and not \
				AllFeedMongo().if_news_exists(news_dict["news_id"], news_dict["news_link"]):
                                self.links_not_present.append(news_dict)
                                print self.links_not_present

                return 


        def full_news(self):
                """
                makes full new of the new_dict and insert into mongodb with following keys
                ['website', 'hdpi', 'tags', 'image_link', 'time_of_storing', 'news', 'ldpi', 'publish_epoch', 'mdpi', 'title', 'summary', 'news_id', 
                'news_link', 'published']
                

                """
            
                goose_instance = Goose()
                for news_dict in self.links_not_present:
           
			if news_dict['published'].endswith("GMT") or news_dict['published'].endswith("+0000"):
                                date = parse(news_dict['published'])
                                datetime_tuple = datetime.timetuple(date)
                                publish_epoch = calendar.timegm(datetime_tuple)
                                day = datetime_tuple.tm_mday
                                month = datetime_tuple.tm_mon
                                year = datetime_tuple.tm_year

                        else:
                                print 'couldn\'t convert'
                                strp_time_object = time.strptime(news_dict['published'], "%Y-%m-%d %H:%M:%S" )
                                publish_epoch = time.mktime(strp_time_object)
                                day = strp_time_object.tm_mday
                                month = strp_time_object.tm_mon
                                year = strp_time_object.tm_year
                        #publish_epoch = time.mktime(strp_time_object)
			gmt_epoch = calendar.timegm(time.gmtime(publish_epoch))                       
 

                        ##Getting full article with goose
                        article = goose_instance.extract(news_dict["news_link"])
                        full_text = unicode_or_bust(article.cleaned_text.format())
            
                        tokenized_data = sent_tokenize(full_text)
                        length_tokenized_data=len(tokenized_data)

                        #if length_tokenized_data > 1:
                                #summary=tokenized_data[0]+tokenized_data[1]+" "+ " ...Read More"
                        if length_tokenized_data > 1:
                                summary = " ".join(word_tokenize(full_text)[:100])+" "+ " ...Read More"
			elif article.meta_description:
                                summary = article.meta_description
			else:
				summary = None

                        try: 
                                image_link = article.opengraph['image']
                                obj1=AmazonS3(image_link, news_dict["news_id"])
                                all_formats_image=obj1.run()
                        except Exception as e:
                                print e
                                image_link = None
                                all_formats_image = {"mdpi": None,
                                                    "ldpi": None,
                                                    "hdpi": None,}

           		summarization_instance = ShortNews() 

			try:
                                news_dict.update({"website": "www.reuters.com", "summary": summarization_instance.summarization(full_text),\
						"custom_summary":summary, "news": full_text, "image_link":image_link,'gmt_epoch':gmt_epoch,'publish_epoch':\
						publish_epoch, "day": day, "month": month, "year": year,'ldpi': all_formats_image['ldpi'],\
						'mdpi': all_formats_image['mdpi'],'hdpi': all_formats_image['hdpi'],"time_of_storing":\
                                                time.mktime(time.localtime()),'type':'cricket','favicon':'https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Reuters_logo.svg/640px-Reuters_logo.svg.png'})
			except:
                                news_dict.update({"website": "www.reuters.com", "summary": summary,\
						"custom_summary":summary, "news": full_text, "image_link":image_link,'gmt_epoch':gmt_epoch,'publish_epoch':\
						publish_epoch, "day": day, "month": month, "year": year,'ldpi': all_formats_image['ldpi'],\
						'mdpi': all_formats_image['mdpi'],'hdpi': all_formats_image['hdpi'],"time_of_storing":\
                                                time.mktime(time.localtime()),'type':'cricket','favicon':'https://upload.wikimedia.org/wikipedia/en/thumb/e/e2/Reuters_logo.svg/640px-Reuters_logo.svg.png'})

                        if news_dict['news'] and not news_dict['summary'] == " ...Read More":
                                print "Inserting news id %s with news link %s"%(news_dict.get("news_id"), news_dict.get("news_link"))
                                CricFeedMongo().insert_news(news_dict)
				print 'here'
				AllFeedMongo().insert_news(news_dict)
			else:
				print 'not stored'
                return                 

    
if __name__ == '__main__':
    obj = CricketReuters(REUT_CRIC_FEED)
    obj.run()
    #obj.rss_feeds(ESPN_CRIC_FEED)
    #obj.checking()
    #obj.full_news()








