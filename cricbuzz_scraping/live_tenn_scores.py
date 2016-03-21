#!/usr/bin/env python

import sys
import os
import json
import feedparser
from goose import Goose
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(parent_dir_path)




class TennisScores(object):
        
        def __init__(self,url):
                
                self.url = url
                self.rss = feedparser.parse(self.url)

        def get_scores(self):
                __dict = dict()
                for value in self.rss.entries:
                        if value['summary']=="P1ret":
                        
                                value['summary']="Player 1 retired"
                        elif value['summary']=="P2ret":
                                value['summary']="Player 2 retired"

                        __dict.update({"date":value['published'],"summary":value['summary'], "score":value['title'][39:].replace('#',"")})
                        #print value['title'][39:].replace('#','')
                        print __dict


def main():
        
        obj = TennisScores('http://www.scorespro.com/rss2/live-tennis.xml')
        obj.get_scores()

if __name__=='__main__':main()



                    
                
