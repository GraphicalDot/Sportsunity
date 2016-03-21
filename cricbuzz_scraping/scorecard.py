#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pymongo

class Scorecard:

	def __init__(self,url,match_description):
                self.match_description = match_description
		res = requests.get(url)
                scorecard_url = res.url.replace('scores','scorecard')
                print scorecard_url
                response = requests.get(scorecard_url)
		self.soup = BeautifulSoup(response.content,'lxml')
                conn = pymongo.MongoClient()
                db = conn.drake
                self.testing = db.testing

		
	def cric_scorecard(self):
		for x in self.soup.find_all('div',{'id':'innings_1'}):
			table=x.find_all('table')
		row=table[0].find_all('tr')
		row_1=table[1].find_all('tr')
                print self.match_description.split(',')[1].strip()
                print "1st inning"
		for stat in row:
			columns=stat.find_all('td')
			if not columns[1].string:
				pass
			elif columns[0].string in ['Extras','Total','Yet to Bat', 'Did not Bat']:
				print columns[0].string,columns[1].string
			else:
                            print 'batsman: '+columns[0].string,'status: '+columns[1].string,'runs_scored: '+columns[2].string,\
                                        'balls_consumed: '+columns[3].string,'fours: '+columns[4].string,'sixes: '+columns[5].string,\
                                        'strike-rate: '+columns[6].string
		for stat_bowl in row_1:
			columns_bowl=stat_bowl.find_all('td')
			if columns_bowl[0].string=='Bowler':
				pass
			else:
				print 'bowler: '+columns_bowl[0].string,'overs: '+columns_bowl[1].string,'maidens: '+columns_bowl[2].string,\
                                        'runs_conceded: '+columns_bowl[3].string,'wickets: '+columns_bowl[4].string,\
                                        'no-balls: '+columns_bowl[5].string,'wides: '+columns_bowl[6].string,'economy: '+columns_bowl[7].string


                if self.soup.find_all('div',{'id':'innings_2'}):
                        print 
                        print "2nd inning"
                        for x in self.soup.find_all('div',{'id':'innings_2'}):
                            table=x.find_all('table')
                        row=table[0].find_all('tr')
                        row_1=table[1].find_all('tr')
                        print self.match_description
                        for stat in row:
                            columns=stat.find_all('td')
                            if not columns[1].string:
                                pass
                            elif columns[0].string in ['Extras','Total','Yet to Bat', 'Did not Bat']:
                                print columns[0].string,columns[1].string
                            else:
                                print 'batsman: '+columns[0].string,'status: '+columns[1].string,'runs_scored: '+columns[2].string,\
                                        'balls_consumed: '+columns[3].string,'fours: '+columns[4].string,'sixes: '+columns[5].string,\
                                        'strike-rate: '+columns[6].string

                        for stat_bowl in row_1:
                            columns_bowl=stat_bowl.find_all('td')
                            if columns_bowl[0].string=='Bowler':
                                pass
                            else:
                                print 'bowler: '+columns_bowl[0].string,'overs: '+columns_bowl[1].string,'maidens: '+columns_bowl[2].string,\
                                        'runs_conceded: '+columns_bowl[3].string,'wickets: '+columns_bowl[4].string,\
                                        'no-balls: '+columns_bowl[5].string,'wides: '+columns_bowl[6].string,'economy: '+columns_bowl[7].string

                else:
                        print "2nd inning yet to start"


        def store_scorecard(self):
                print "inside store_scorecard"
                for match in self.testing.find():
                        match_number = self.match_description.split(',')[1].strip() 
                        match_name = self.match_description.split(',')[0]
                        if match['match_desc'].replace('vs','v').lower() == match_name.lower() and match['mch_num'] == \
                                match_number:
                                print match
                    



"""
if __name__=='__main__':
	obj = Scorecard('http://www.cricbuzz.com/live-cricket-scorecard/15393/zim-vs-ire-1st-odi-ireland-tour-of-zimbabwe-2015')
	obj.cric_scorecard()
"""			
				
