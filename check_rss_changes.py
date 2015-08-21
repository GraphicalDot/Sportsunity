#!/usr/bin/env python

__metaclass__ = type

import os
import sys
parent_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir_path)
from notify_rss_changes import NotifyingRssChanges
from GlobalLinks import *

class SportsRssLinks:

        def __init__(self):
                pass

        def check(self, url):
                self.url = url
                print self.url
                notify_rss_changes_instance = NotifyingRssChanges(self.url)
                #if notify_rss_changes_instance.check_rss():
                notify_rss_changes_instance.send_notification()



class CheckRssKeys(SportsRssLinks):

        def send_basketball_keys(self):
                for link in [NBA,Real_gm,Roto_world,Inside_hoops]:
                        self.check(self.url)


        def send_cricket_keys(self):
                for link in [NDTV_CRICKET_FEED, ESPN_CRIC_FEED, BBC_CRIC_FEED, CBUZ_CRIC_FEED]:
                        self.check(link)


        def send_football_keys(self):
                for link in [Fifa_dot_com, Football_Fancast, Football_uk, Goal_dot_com]:
                        self.check(link)


        def send_formula1_keys(self):
                for link in [Crash_dot_net, Grandprix_dot_com, Auto_sport]:
                        self.check(link)


        def send_tennis_keys(self):
                for link in [WTA, TENNIS_X, BBC_FEED]:
                        self.check(link)


if __name__=='__main__':
        obj = CheckRssKeys()
        #obj.send_basketball_keys()
        #obj.send_cricket_keys()
        #obj.send_football_keys()
        obj.send_formula1_keys()
        obj.send_tennis_keys()
