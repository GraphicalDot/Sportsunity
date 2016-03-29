#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.abspath(os.path.abspath(__file__)))

from GlobalConfigs  import news_collection_tenn
from Feeds.mongo_feed_handler import MongoFeedHandler


class TennFeedMongo(MongoFeedHandler):
    """

    """
    def __init__(self):
        self.collection = news_collection_tenn
        super(TennFeedMongo, self).__init__()
