#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import pprint
import termcolor
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class BattingRecords:

        def __init__(self):
                conn = connection.get_mongo_connection()
                # db = conn.admin
                # db.authenticate('shivam','mama123')
                db = conn.stats
                self.player_stats = db.player_stats
                self.stats_list = list()
                for x in range(1,10):
                    self._dict1 = {}
                    response = requests.get('http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;spanmax2=18+Jan+2016;spanmin2=18+Jan+2015;spanval2=span;team={0};template=results;type=batting'.format(x))
                    self.soup = BeautifulSoup(response.content,"lxml")
                    res = requests.get("http://stats.espncricinfo.com/ci/engine/stats/index.html?class=2;spanmax2=18+Jan+2016;spanmin2=18+Jan+2015;spanval2=span;team={0};template=results;type=bowling".format(x))
                    self.soup1 = BeautifulSoup(res.content,"lxml")
                    self.bowling_cricket()
                    self.batting_cricket()

        def bowling_cricket(self):
                team = self.soup1.find('table',{'class':'engineTable'})
                print termcolor.colored(team.findAll('td')[1].get_text().split('team')[1],"blue")
                for data in self.soup1.find_all('table',{'class':'engineTable'}):
                        try:
                            body=data.find_all('tbody')
                            for stats in body:
                                rows = stats.find_all('tr')
                        except:
                            pass

                for row in rows:
                        stat=row.find_all('td')
                        try:
                                self.player_stats.update({'team':team.findAll('td')[1].get_text().split('team')[1].strip(),'player':stat[0].string,'type':\
                                        'bowling'},{'$set':{'player':stat[0].string,'matches':stat[1].string,'inngs':\
                                        stat[2].string,'overs':float(stat[3].string),'maidens':stat[4].string,'runs':int(stat[5].string),'type':'bowling','wickets':\
                                        stat[6].string,'average':float(stat[8].string),'economy':float(stat[9].string),'strike_rate':float(stat[10].string)}},upsert=True)

                                _dict ={'player':stat[0].string,'matches':stat[1].string,'inngs':\
                                        stat[2].string,'overs':float(stat[3].string),'maidens':stat[4].string,'runs':int(stat[5].string),'wickets':\
                                        stat[6].string,'average':float(stat[8].string),'economy':float(stat[9].string),'strike_rate':float(stat[10].string)}
                        except Exception as e:
                                self.player_stats.update({'team':team.findAll('td')[1].get_text().split('team')[1].strip(),'player':stat[0].string,'type':\
                                        'bowling'},{'$set':{'player':stat[0].string,'matches':stat[1].string,'inngs':\
                                        stat[2].string,'overs':stat[3].string,'maidens':stat[4].string,'runs':stat[5].string,'type':'bowling','wickets':\
                                        stat[6].string,'average':stat[8].string,'economy':stat[9].string,'strike_rate':stat[10].string}},upsert=True)

                                _dict ={'player':stat[0].string,'match':stat[1].string,'inngs':\
                                        stat[2].string,'overs':stat[3].string,'maidens':stat[4].string,'runs':stat[5].string,'wickets':\
                                        stat[6].string,'average':stat[8].string,'economy':stat[9].string,'strike_rate':stat[10].string}

                        #self._dict1.setdefault(team.findAll('td')[1].get_text().split('team')[1].strip(),{}).setdefault("bowling",[]).append(_dict)


        def batting_cricket(self):
                team = self.soup.find('table',{'class':'engineTable'})
                print team.findAll('td')[1].get_text().split('team')[1]
                for data in self.soup.find_all('table',{'class':'engineTable'}):
                        try:
                            body=data.find_all('tbody')
                            for stats in body:
                                rows = stats.find_all('tr')
                        except:
                            pass

                for row in rows:
                        stat=row.find_all('td')
                        try:
                                self.player_stats.update({'team':team.findAll('td')[1].get_text().split('team')[1].strip(),'player':stat[0].string,'type':\
                                        'batting'},{'$set':{'player':stat[0].string,'match':stat[1].string,'inngs':\
                                        stat[2].string,'notouts':stat[3].string,'runs':int(stat[4].string),'highest':stat[5].string,'type':'batting','average':\
                                        float(stat[6].string), 'strike_rate':float(stat[8].string), '100s':stat[9].string, '50s':stat[10].string, '0s':\
                                        stat[11].string,'4s':stat[12].string, '6s':stat[13].string}},upsert=True)

                                _dict ={'player':stat[0].string,'match':stat[1].string,'inngs':\
                                        stat[2].string,'notouts':stat[3].string,'runs':int(stat[4].string),'highest':stat[5].string, 'average':\
                                        float(stat[6].string), 'strike_rate':float(stat[8].string), '100s':stat[9].string, '50s':stat[10].string, '0s':\
                                        stat[11].string,'4s':stat[12].string, '6s':stat[13].string}
                        except Exception as e:
                                self.player_stats.update({'team':team.findAll('td')[1].get_text().split('team')[1].strip(),'player':stat[0].string,'type':\
                                        'batting'},{'$set':{'player':stat[0].string,'match':stat[1].string,'inngs':\
                                        stat[2].string,'notouts':stat[3].string,'runs':stat[4].string,'highest':stat[5].string,'type':'batting','average':\
                                        stat[6].string, 'strike_rate':stat[8].string, '100s':stat[9].string, '50s':stat[10].string, '0s':\
                                        stat[11].string,'4s':stat[12].string, '6s':stat[13].string}},upsert=True)

                                _dict ={'player':stat[0].string,'match':stat[1].string,'inngs':\
                                        stat[2].string,'notouts':stat[3].string,'runs':stat[4].string,'highest':stat[5].string,'average':\
                                        stat[6].string, 'strike_rate':stat[8].string, '100s':stat[9].string, '50s':stat[10].string, '0s':\
                                        stat[11].string,'4s':stat[12].string, '6s':stat[13].string}

                        #self._dict1.setdefault(team.findAll('td')[1].get_text().split('team')[1].strip(),{}).setdefault("batting",[]).append(_dict)



                #pprint.pprint(self._dict1)
                        #self.stats_list.append(_dict)

                #pprint.pprint(self.stats_list)

if __name__=='__main__':
        obj = BattingRecords()
        obj.bowling_cricket()
        obj.batting_cricket()
