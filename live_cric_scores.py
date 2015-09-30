#!/usr/bin/env python

import os
import sys
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from urllib2 import urlopen
from bs4 import BeautifulSoup
import pymongo
import time
import feedparser
from operator import itemgetter
from goose import Goose

class CricketScores:
        def __init__(self,url):

                content = urlopen(url).read()
                self.soup = BeautifulSoup(content,"lxml")
                conn = pymongo.MongoClient()
                db = conn.drake
                self.testing = db.testing
                self.pattern = "%b %d %Y"

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
                                        inning[0].get('wkts'),'overs':inning[0].get('ovrs'),'date_time':date_time[0].get('dt')}},upsert = True)


                                #self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{"match_day_epoch":match_day_epoch}})
                        except:
                                self.testing.update({'match_desc':match.get('mchdesc')},{'$set':{'match_desc':match.get('mchdesc'),'mch_num':\
                                        match.get('mnum'),'status':state[0].get('status'),'date_time':date_time[0].get('dt')}},upsert = True)
                                

        def show_scores(self):
                for score in self.testing.find(projection={'_id':False}):
                        try:
                                match_day_epoch = int(time.mktime(time.strptime(score['match_day_epoch'], self.pattern)))
                                self.testing.update({'mch_num':score['mch_num'],'match_desc':score['match_desc']},{'$set':{"match_day_epoch":\
                                        match_day_epoch}})
                        except:
                                pass

                        print score

        def send_scores(self, match_date):
                "Checks whether the date matches the date entered\
                        and sends the scores of ongoing match"

                all_scores = []
                for score in self.testing.find(projection={'_id':False, 'live_commentary':False}):
                        try:
                            if score['match_day_epoch'] == match_date:
                                    all_scores.append(score)
                        except:
                                pass
                return all_scores


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
                                self.cric_fixtures.update({'match_desc':fix['match_desc']},{'$set':{'fixture_day_epoch':epoch}})

                        else:
                                epoch= time.mktime(time.strptime(fix['Date'],"%a %d %b,%Y "))
                                self.cric_fixtures.update({'match_desc':fix['match_desc']},{'$set':{'fixture_day_epoch':epoch}})

                        if epoch<time.time():
                                self.cric_fixtures.remove(fix)
                        else:
                                pass

        def show_fixtures(self):
                
                "Shows all the fixtures and the count"
                
                for fix in self.cric_fixtures.find(projection={'_id':False}):
                        print fix
                print self.cric_fixtures.count()

        def send_fixtures_if_no_date(self):
                upcoming_ten_fixtures = []
                for fixture in self.cric_fixtures.find(projection={'_id':False}).sort('fixture_day_epoch',1).limit(10):
                        try:
                            upcoming_ten_fixtures.append(fixture)
                        except:
                            pass

                return upcoming_ten_fixtures
                        


        def send_fixtures(self, fixture_date):

                "Checks whether the date entered matches todays date\
                        and sends the fixtures for the current date"    

                fixtures_for_today = []
                for fixture in self.cric_fixtures.find(projection={'_id':False}):
                        try:
                            if fixture_date == fixture['fixture_day_epoch']:
                                    fixtures_for_today.append(fixture)
                        except:
                            pass
                return fixtures_for_today


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
                
                for rss in self.feeds.entries:
                        if 'Partnership' in rss['summary'] or 'MoM' in rss['summary']:
                                data = self.goose_instance.extract(rss['link'])
                                self.commentary = data.cleaned_text.split('\n')
                                self.match_name = rss['title'].split(',')[0]

                                for self.match in self.testing.find():
                                        if self.match['match_desc'].replace('vs','v').lower() == self.match_name.lower():
                                                self.get_commentary()
                                        else:
                                                pass



        def get_commentary(self):

                """Gets the commentary of live match\
                    from rss feeds"""

            
                try:
                        self.number_of_entries = len(self.match['live_commentary'])
                except:
                        pass

                for comment in self.commentary:
                        if comment == '':
                                pass
                        else:
                                try:
                                        if comment in self.match['live_commentary']:
                                                pass
                                except Exception, e:
                                        print e
                                try:
                                        if int(comment[:1]) in xrange(1,10):
                                                self.testing.update({'mch_num':self.match['mch_num'], 'match_desc':self.match['match_desc']},\
                                                        {'$addToSet':{'live_commentary':{'status':self.match['status'],'runs':\
                                                        self.match['runs'],'wickets':self.match['wkts'],'overs':self.match['overs'],\
                                                        comment[:5]:comment[5:],'time':time.time()}}}, upsert = True)

                                except:
                                        self.testing.update({'mch_num':self.match['mch_num'], 'match_desc':self.match['match_desc']},\
                                                {'$addToSet':{'live_commentary':{'status':self.match['status'],'runs':self.match['runs'],\
                                                'wickets':self.match['wkts'],'overs':self.match['overs'],'comment':comment,'time':\
                                                time.time()}}}, upsert = True)


                try:
                        if len(self.match['live_commentary']) >= self.number_of_entries:
                                self.send_commentary()
                except:
                        print 'no new comment'

                        


                        
        
        def send_commentary(self):
                
                try:
                        latest_comment = self.match['live_commentary']
                        duh = sorted(latest_comment, key = itemgetter('time'))
                        print duh[0]
                except Exception, e:
                        print e
                        
                    


        def show_commentary(self,match):
                """Returns the commentary.Used for API, if query entered is any one of the following\
				aus vs eng, eng vs aus, aus_vs_eng or eng_vs_aus."""
                                
                print match
                
                for comm in self.testing.find():
                        if match.replace('_',' ').lower()==comm['match_desc'].lower() or match.replace('_',' ').lower()==" "\
                                .join(reversed(comm['match_desc'].split(' '))).lower():
                                        
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
        obj2.check_match()
        #obj2.get_commentary()
        #obj2.store_commentary()
        #obj2.store_commentary()

                                    
if __name__=='__main__':main()


                                

                
                
