#!/usr/bin/env python

import os
import sys
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pymongo

class CricketScores:
        def __init__(self,url):

                content = urlopen(url).read()
                self.soup = BeautifulSoup(content,"lxml")
                conn = pymongo.MongoClient()
                db = conn.drake
                self.testing = db.testing

        def get_scores(self):
                for match in self.soup.find_all('match'):
                        state= match.find_all('state')
                        inning= match.find_all('inngs')
                        batting= match.find_all('bttm')
                        bowling= match.find_all('blgtm')
                        #if inning and batting and bowling:
                        try:
                                self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{'match_desc':match.get('mchdesc'),'mch_num':\
                                        match.get('mnum'),'status':state[0].get('status'),"bttng":batting[0].get('sname'),"blng":\
                                        bowling[0].get('sname')}},upsert = True)
                        except:
                                self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{'match_desc':match.get('mchdesc'),'mch_num':\
                                        match.get('mnum'),'status':state[0].get('status')}},upsert = True)

        def show_scores(self):
                for score in self.testing.find(projection={'_id':False}):
                        print score

class CricketFixtures:
        def __init__(self,url):
                
                content = urlopen(url).read()
                self.soup = BeautifulSoup(content,"lxml")
                conn = pymongo.MongoClient()
                db = conn.drake
                self.cric_fixtures = db.cric_fixtures

        def get_fixtures(self):
                
                for fixture in self.soup.find_all('mch'):
                        self.cric_fixtures.update({'match_desc':fixture.get('desc')},{'$set':{'match_desc':fixture.get('desc'), 'tournament':\
                                fixture.get('srs')[5:], 'Venue':fixture.get('vnu'), 'Date':fixture.get('ddt')+ " "+fixture.get('mnth_yr'),\
                                'time':fixture.get('tm')}},upsert = True)

        def show_fixtures(self):
                for fix in self.cric_fixtures.find(projection={'_id':False}):
                        print fix
                print self.cric_fixtures.count()



def main():
        obj = CricketScores('http://synd.cricbuzz.com/j2me/1.0/livematches.xml')
        obj.get_scores()
        obj.show_scores()
        print '\n'
        obj1 = CricketFixtures('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')
        obj1.get_fixtures()
        obj1.show_fixtures()

                                    
if __name__=='__main__':main()


                                

                
                
