#!/usr/bin/env python

import sys
import os
import json
import feedparser
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)




class CricketScores(object):
        
        def __init__(self,url):
                
                self.url = url
                self.rss = feedparser.parse(self.url)


                    
                
