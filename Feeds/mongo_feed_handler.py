#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.abspath(os.path.abspath(__file__)))


class MongoFeedHandler(object):
    """

    """

    def if_news_exists(self, news_id, news_link):
        if self.collection.find_one({"news_id": news_id, "news_link": news_link}):
            return True
        return False

    def insert_news(self, news_dict):
        self.collection.insert(news_dict)
        return
