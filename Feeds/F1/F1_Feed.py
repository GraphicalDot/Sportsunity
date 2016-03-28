import sys
import os
import feedparser
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from mongo_db_formulaone import FormFeedMongo
from Feeds.All.mongo_db_all import AllFeedMongo
import GlobalLinks
import hashlib


class MainF1FeedHandler:
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
            if not FormFeedMongo().if_news_exists(news_dict["news_id"], news_dict["news_link"]) and not \
                    AllFeedMongo().if_news_exists(news_dict["news_id"], news_dict["news_link"]):
                self.links_not_present.append(news_dict)

        return
