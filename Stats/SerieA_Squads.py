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

                print  
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
        list_of_teams = ['atalanta','bologna','carpi','chievo','empoli','fiorentina','frosinone','genoa','hellas-verona','internazionale',\
                'juventus','lazio','milan','napoli','palermo','roma','sampdoria','sassuolo','torino','udinese']

        list_of_ids = ['/1255?ICID=SP_TN_90','/1249?ICID=SP_TN_91','/12140?ICID=TP_TN_92','/1248?ICID=TP_TN_93','/1261?ICID=TP_TN_94',\
                '/1259?ICID=TP_TN_95','/2981?ICID=TP_TN_96','/1276?ICID=TP_TN_97','/1277?ICID=TP_TN_98','/1244?ICID=TP_TN_99',\
                '/1242?ICID=TP_TN_100','/1245?ICID=TP_TN_101','/1240?ICID=TP_TN_102','/1270?ICID=TP_TN_103','/1254?ICID=TP_TN_104',\
                '/1241?ICID=TP_TN_105','/1247?ICID=TP_TN_106','/5681?ICID=TP_TN_107','/1268?ICID=TP_TN_108','/1246?ICID=TP_TN_109']

        for team,_id in izip(list_of_teams,list_of_ids):
            url = 'http://www.goal.com/en-us/teams/italy/serie-a/13/'+team+_id
            obj = Squads(url,team)
            obj.get_squads()


if __name__=='__main__':main()
