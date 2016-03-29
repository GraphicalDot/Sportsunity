#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.abspath(os.path.abspath(__file__)))

from GlobalConfigs import news_collection_cric
from Feeds.mongo_feed_handler import MongoFeedHandler


class CricFeedMongo(MongoFeedHandler):
    """

    """
    def __init__(self):
        self.collection = news_collection_cric
        super(CricFeedMongo, self).__init__()
