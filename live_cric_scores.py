#!/usr/bin/env python

import os
import sys
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pymongo
import time
import feedparser
from goose import Goose

class CricketScores:
        def __init__(self,url):

                content = urlopen(url).read()
                self.soup = BeautifulSoup(content,"lxml")
                conn = pymongo.MongoClient()
                db = conn.drake
                self.testing = db.testing

        def get_scores(self):
		"""Gets live scores and updates in the database"""

                for match in self.soup.find_all('match'):
                        state= match.find_all('state')
                        inning= match.find_all('inngs')
                        batting= match.find_all('bttm')
                        bowling= match.find_all('blgtm')
                        date_time= match.find_all('tme')
                        #if inning and batting and bowling:
                        try:
                                self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{'match_desc':match.get('mchdesc'),'mch_num':\
                                        match.get('mnum'),'status':state[0].get('status'),'additional':state[0].get('addnstatus'),"bttng":\
                                        batting[0].get('sname'),"blng":bowling[0].get('sname'),'runs':inning[0].get('r'),'wkts':\
                                        inning[0].get('wkts'),'overs':inning[0].get('ovrs')}},upsert = True)
                        except:
                                self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{'match_desc':match.get('mchdesc'),'mch_num':\
                                        match.get('mnum'),'status':state[0].get('status'), 'date_time':date_time[0].get('dt')}},upsert = True)

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
                """Gets all the fixtures"""

                for fixture in self.soup.find_all('mch'):
                        self.cric_fixtures.update({'match_desc':fixture.get('desc')},{'$set':{'match_desc':fixture.get('desc'), 'tournament':\
                                fixture.get('srs')[5:], 'Venue':fixture.get('vnu'), 'Date':fixture.get('ddt')+" "+fixture.get('mnth_yr'),'time':\
                                fixture.get('tm')}},upsert = True)

        def update_fixtures(self):
		"""Removes fixtures that are completed"""

                for fix in self.cric_fixtures.find(projection={'_id':False}):
                        if len(fix['Date'])>17:
                                epoch= time.mktime(time.strptime(fix['Date'].split('- ')[1],"%a %d %b,%Y "))
                        else:
                                epoch= time.mktime(time.strptime(fix['Date'],"%a %d %b,%Y "))
                        if epoch<time.time():
                                self.cric_fixtures.remove(fix)
                        else:
                                pass

        def show_fixtures(self):
                for fix in self.cric_fixtures.find(projection={'_id':False}):
                        print fix
                print self.cric_fixtures.count()


class CricketCommentary:

        def __init__(self,url):

		conn = pymongo.MongoClient()
		db = conn.drake
		self.testing = db.testing
                self.goose_instance = Goose()
                self.feeds = feedparser.parse(url)

	def check_match(self):
		"""Makes sure that we fetch the commentary for\
				the match that is going on"""

		for match in self.testing.find():
			for rss in self.feeds.entries:
				if match['match_desc'].replace('vs','v').lower() in rss['title'].lower():
                                        return "There is a match on" 
				else:
					pass


        def get_commentary(self):
		"""Gets the commentary of live match\
				from rss feeds"""
            
                if self.check_match():
                        print 'inside get_comm'
                        self._dict = dict()
                        _dict1 = dict()
                        commentary = []
                        teams = []
                        #for match in self.testing.find():

                        for rss in self.feeds.entries:
                                if "Partnership" in rss.summary or "MoM" in rss.summary:
                                                text = self.goose_instance.extract(rss['link'])
                                                teams.append(rss['title'])
                                                commentary.append(text.cleaned_text.split('\n'))
                                                for index in range(len(teams)):
                                                        for comm in commentary[index]:
                                                                if comm == " ":
                                                                        pass
                                                                else:
                                                                        try:
                                                                                if int(comm[:1]) in xrange(1,10):
                                                                                        _dict1.update({comm[:4].replace('.','period'):comm[5:]})
                                                                                self._dict.update({teams[index]:_dict1})
                                                                        except:
                                                                                pass

                                                                                                                          

                        print self._dict


        def store_commentary(self):
                for match in self.testing.find():
                        for key in self._dict.viewkeys():
                                if match['match_desc'].replace('vs','v').lower() in key.lower():
                                        self.testing.update({'match_desc':match['match_desc']},{'$set':{'commentary':self._dict}})
                                        print 'stored'
                                else:
                                        pass




	def show_commentary(self,match):
		"""Returns the commentary.Used for API, if query entered is any one of the following\
				aus vs eng, eng vs aus, aus_vs_eng or eng_vs_aus."""

		print match

		for comm in self.testing.find():
			if match.replace('_',' ').lower()==comm['match_desc'].lower() or match.replace('_',' ').lower()==\
					" ".join(reversed(comm['match_desc'].split(' '))).lower():
				return comm['commentary']

                        

def main():
        obj = CricketScores('http://synd.cricbuzz.com/j2me/1.0/livematches.xml')
        obj.get_scores()
        obj.show_scores()
        print '\n'
        obj1 = CricketFixtures('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')
        obj1.get_fixtures()
        obj1.update_fixtures()
        obj1.show_fixtures()
        print '\n'
        obj2 = CricketCommentary('http://live-feeds.cricbuzz.com/CricbuzzFeed?format=xml')
        #obj2.check_match()
        obj2.get_commentary()
        obj2.store_commentary()
        #obj2.store_commentary()

                                    
if __name__=='__main__':main()


                                

                
                
