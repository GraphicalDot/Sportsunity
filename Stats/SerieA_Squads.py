#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
import termcolor
import hashlib
from itertools import izip
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


reload(sys)
sys.setdefaultencoding('utf-8')

class SerieASquads:
        
        def __init__(self,link,team):
                res = requests.get(link)
                self.soup = BeautifulSoup(res.content,"lxml")
                self.team = team
                conn = connection.get_mongo_connection()
                # db = conn.admin
                # db.authenticate('shivam','mama123')
                db = conn.football
                self.football_player_stats = db.football_player_stats

        def get_squads(self):
                table = self.soup.findAll('table',{'class':'tab-squad tab-squad-players'})

                rows=table[0].find_all('tr')

                print termcolor.colored(self.team.upper(),"red")
                print 
                for row in rows:
                        name = row.find('td',{'class':'name'})
                        image=row.find('img')
                        self.squad=row.find_all('td')
                        try:
                            link=name.find('a')
                            self.get_football_player_stats('http://www.goal.com/'+link.get('href'))
                            print self.squad[2].text
                            if self.list_of_profile:

                                self.football_player_stats.update({'short_name':self.squad[2].text.strip(),'team_name':self.team},{'$set':{'player_image':self.player_image,'name':self.name.text.strip(),'full_name_id':\
                                        hashlib.md5(self.name.text.strip()).hexdigest(),'team_id':hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'team':" ".join(self.team.split('-')).title(),'team_name':\
                                        self.team,'Jersey':self.squad[1].string.strip(),'short_name':self.squad[2].text.strip(),'player_id':hashlib.md5(self.squad[2].text.strip()+self.squad[1].string.strip()).hexdigest(),\
                                        'Nationality':self.squad[3].find('span').get('title'),'Position':self.squad[4].string.strip(),'image':image.get('src'),'Age':self.squad[5].string.strip(),'Games':\
                                        self.squad[6].string.strip(),'Goals':self.squad[7].string.strip(),'Assists':self.squad[8].string.strip(),'Yellow':self.squad[9].string.strip(),'Red':\
                                        self.squad[11].string.strip(),'profile':self.list_of_profile,'other_competitions':self.list_of_other_competitions,'competition_name':'SerieA','sport_type':'football'}},upsert=True)
                            else:
                                self.football_player_stats.update({'short_name':self.squad[2].text.strip(),'team_name':self.team},{'$set':{'player_image':'','name':self.squad[2].text.strip(),'full_name_id':\
                                        hashlib.md5(self.squad[2].text.strip()).hexdigest(),'team_id':hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'team':" ".join(self.team.split('-')).title(),'team_name':\
                                        self.team,'Jersey':self.squad[1].string.strip(),'short_name':self.squad[2].text.strip(),'player_id':hashlib.md5(self.squad[2].text.strip()+self.squad[1].string.strip()).hexdigest(),\
                                        'Nationality':self.squad[3].find('span').get('title'),'Position':self.squad[4].string.strip(),'image':image.get('src'),'Age':self.squad[5].string.strip(),'Games':\
                                        self.squad[6].string.strip(),'Goals':self.squad[7].string.strip(),'Assists':self.squad[8].string.strip(),'Yellow':self.squad[9].string.strip(),'Red':\
                                        self.squad[11].string.strip(),'profile':self.list_of_profile,'other_competitions':self.list_of_other_competitions,'competition_name':'SerieA','sport_type':'football'}},upsert=True)

                        except Exception,e:
                            print e
                            pass
                            
                manager = self.soup.find('table',{'class':'tab-squad tab-squad-manager'})
                manager_name = manager.find_all('td')
                self.image = manager_name[0].find('img')
                print 
                #print image.get('src') 
                print manager_name[1].text 


        def get_football_player_stats(self,link):
                res = requests.get(link)
                soup = BeautifulSoup(res.content)
                self.list_of_other_competitions = []
                self.list_of_profile = []
                try:
                    self.name=soup.findAll('div',{'id':'playerStatsCard'})[0].find('td',{'class':'playerName'})

                    stat_table = soup.findAll('div',{'class':'playerGameStatsContainer'})

                    image = soup.findAll('td',{'class':'playerPicture'})[0].find('img').get('src')

                    if not 'dummy' in image:
                            self.player_image = image
                    else:
                            pass


                    try:
                        self.list_of_profile.append({soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[0].text.replace(':',''):soup.findAll('div',{'id':\
                                    'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[1].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[1].text.replace(':',''):\
                                                    soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[2].text,soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':\
                                                    'playerStatLabel'})[2].text.replace(':',''):soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[3].text.strip(),\
                                                    soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[3].text.replace(':',''):soup.findAll('div',{'id':\
                                                        'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[4].text})
                    except Exception,e:

                        self.list_of_profile.append({soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[0].text.replace(':',''):soup.findAll('div',{'id':\
                                    'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[1].text.strip(),soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatLabel'})[1].text.replace(':',''):\
                                                    soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[2].text.strip(),soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':\
                                                    'playerStatLabel'})[2].text.replace(':',''):soup.findAll('div',{'id':'playerStatsCard'})[0].findAll('td',{'class':'playerStatValue'})[3].text.strip()})
                    
                    for stat in stat_table[0].findAll('tr'):
                        column = stat.findAll('td')
                        try:
                            self.list_of_other_competitions.append({'league':column[0].text,'team':column[1].text,'games':column[2].text,'goals':column[3].text,'assists':column[4].text,'yellow_card':\
                                    column[5].text,'red_card':column[6].text})
                        except Exception,e:
                            pass

                except Exception,e:
                    pass

                return



def main():
        list_of_teams = ['atalanta','bologna','carpi','chievo','empoli','fiorentina','frosinone','genoa','hellas-verona','internazionale',\
                'juventus','lazio','milan','napoli','palermo','roma','sampdoria','sassuolo','torino','udinese']

        list_of_ids = ['/1255?ICID=SP_TN_90','/1249?ICID=SP_TN_91','/12140?ICID=TP_TN_92','/1248?ICID=TP_TN_93','/1261?ICID=TP_TN_94',\
                '/1259?ICID=TP_TN_95','/2981?ICID=TP_TN_96','/1276?ICID=TP_TN_97','/1277?ICID=TP_TN_98','/1244?ICID=TP_TN_99',\
                '/1242?ICID=TP_TN_100','/1245?ICID=TP_TN_101','/1240?ICID=TP_TN_102','/1270?ICID=TP_TN_103','/1254?ICID=TP_TN_104',\
                '/1241?ICID=TP_TN_105','/1247?ICID=TP_TN_106','/5681?ICID=TP_TN_107','/1268?ICID=TP_TN_108','/1246?ICID=TP_TN_109']

        for team,_id in izip(list_of_teams,list_of_ids):
            url = 'http://www.goal.com/en-us/teams/italy/serie-a/13/'+team+_id
            obj = SerieASquads(url,team)
            obj.get_squads()


if __name__=='__main__':main()
