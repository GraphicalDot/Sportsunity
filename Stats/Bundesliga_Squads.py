#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import termcolor
from itertools import izip
class Squads:
        
        def __init__(self,link,team):
                res = requests.get(link)
                self.soup = BeautifulSoup(res.content,"lxml")
                self.team = team
                
        def get_squads(self):
                for s in self.soup.find_all('table',{'class':'tab-squad tab-squad-players'}):
                    rows=s.find_all('tr')
                
                print termcolor.colored(self.team.upper(),"red")
                print 
                for row in rows:
                        squad=row.find_all('td')
                        try:
                            print 'Jersey: '+squad[1].string,'Name: '+squad[2].text,'Nationality: '+squad[3].find('span').get('title'),\
                                    'Position: '+squad[4].string
                            print 'Age: '+squad[5].string,'Games: '+squad[6].string,'Goals: '+squad[7].string,'Yellow: '+squad[9].string,'Red:\
                                    '+squad[11].string
                        except:
                            pass

def main():
        list_of_teams = ['augsburg','bayer-leverkusen','bayern-munchen','borussia-dortmund','borussia-mgladbach',\
                'darmstadt-98','eintracht-frankfurt','hamburger-sv','hannover-96','hertha-bsc','hoffenheim',\
                'ingolstadt','koln','mainz-05','hoffenheim','schalke-04','stuttgart','werder-bremen','wolfsburg']

        list_of_ids = ['/1000?ICID=TP_TN_90','/963?ICID=TP_TN_91','/961?ICID=TP_TN_99','/964?ICID=SP_TN_93',\
                '/971?ICID=TP_TN_94','/2549?ICID=TP_TN_95','/979?ICID=TP_TN_103','/967?ICID=TP_TN_104',\
                '/972?ICID=TP_TN_98','/974?ICID=TP_TN_99','/1001?ICID=TP_TN_119','/5476?ICID=TP_TN_120','/980?ICID=TP_TN_121',\
                '/977?ICID=TP_TN_122','/1001?ICID=TP_TN_119','/966?ICID=TP_TN_123','/962?ICID=TP_TN_124','/960?ICID=TP_TN_125',\
                '/968?ICID=TP_TN_126']

        for team,_id in izip(list_of_teams,list_of_ids):
            url = 'http://www.goal.com/en-us/teams/germany/bundesliga/9/'+team+_id
            obj = Squads(url,team)
            obj.get_squads()


if __name__=='__main__':main()
