#!/usr/bin/env python

import sys
import os
import time
import calendar
from nltk.tokenize import sent_tokenize, word_tokenize
from goose import Goose
import GlobalLinks
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mongo_db_basketball import BaskFeedMongo
from Feeds.All.mongo_db_all import AllFeedMongo
from GlobalMethods import unicode_or_bust
from Feeds.amazon_s3 import AmazonS3
from summarize_news import ShortNews
from Basketball_Feed import MainBasketBallFeedHandler


class BasketballHoops(MainBasketBallFeedHandler):
    """
    This function gets the links of all the news articles on the Rss Feed and stores them in list_of_links.
    """

    def full_news(self):
        """
        makes full new of the new_dict and insert into mongodb with following keys
        ['website', 'hdpi', 'tags', 'image_link', 'time_of_storing', 'news', 'ldpi', 'publish_epoch', 'mdpi', 'title', 'summary', 'news_id',
        news_link', 'published']
        """
        goose_instance = Goose()
        for news_dict in self.links_not_present:
            published_news = news_dict['published']
            if published_news.endswith(("+0530", "+0000")):
                strp_time_object = time.strptime(published_news[:-6], "%a, %d %b %Y %H:%M:%S")
            elif published_news.endswith(("GMT", "EDT", "EST")):
                strp_time_object = time.strptime(published_news[:-6], "%a, %d %b %Y %H:%M:%S")
            else:
                strp_time_object = time.strptime(published_news, "%Y-%m-%d %H:%M:%S" )

            day = strp_time_object.tm_mday
            month = strp_time_object.tm_mon
            year = strp_time_object.tm_year
            publish_epoch = time.mktime(strp_time_object)
            gmt_epoch = calendar.timegm(time.gmtime(publish_epoch))

            ##Getting full article with goose
            article = goose_instance.extract(news_dict["news_link"])
            full_text = unicode_or_bust(article.cleaned_text.format())
            favicon = article.infos['meta']['favicon']

            tokenized_data = sent_tokenize(full_text)
            length_tokenized_data=len(tokenized_data)

            if length_tokenized_data > 1:
              summary = " ".join(word_tokenize(full_text)[:100])+" "+ " ...Read More"
            elif article.meta_description:
                summary = article.meta_description+ " "+ " ...Read More"
            else:
                summary = None

            try:
                image_link = article.opengraph['image']
                all_formats_image=AmazonS3(image_link, news_dict["news_id"]).run()
            except Exception as e:
                print e
                image_link = None
                all_formats_image = {"mdpi": None,
                                     "ldpi": None,
                                     "hdpi": None,}

            summarization_instance = ShortNews()

            news_dict.update({
                "website": "www.insidehoops.com",
                "custom_summary": summary,
                "news": full_text,
                "image_link": image_link,
                'gmt_epoch': gmt_epoch,
                'publish_epoch': publish_epoch,
                "day": day,
                "month": month,
                "year": year,
                'ldpi': all_formats_image['ldpi'],
                'mdpi': all_formats_image['mdpi'],
                'hdpi': all_formats_image['hdpi'],
                "time_of_storing": time.mktime(time.localtime()),
                'type':'basketball',
                'favicon':'http://www.insidehoops.com/favicon.ico'})
            try:
                news_dict.update({'summary': summarization_instance.summarization(full_text)})
            except:
                news_dict.update({'summary': summary})

            if full_text != " " and news_dict['summary'] != " ...Read More":
                print "Inserting news id %s with news link %s" % (news_dict.get("news_id"), news_dict.get("news_link"))
                BaskFeedMongo().insert_news(news_dict)
                print 'here'
                AllFeedMongo().insert_news(news_dict)

        return

    
if __name__ == '__main__':
    obj = BasketballHoops(GlobalLinks.Inside_hoops).run()
    sys.exit()
