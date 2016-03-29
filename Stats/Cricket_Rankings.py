#!/usr/bin/env python


from bs4 import BeautifulSoup
import requests
import pprint
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class CricketRanking:

        def __init__(self):
                res = requests.get('http://www.espncricinfo.com/rankings/content/page/211271.html')
                self.soup = BeautifulSoup(res.content,'lxml')
                self.test_list = list()
                self.odi_list = list()
                self.t20_list = list()
                connection = connection.get_mongo_connection()
                db = connection.admin
                db.authenticate('shivam','mama123')
                db = connection.drake
                self.cricket_stats = db.cricket_stats
                db1 = connection.admin
                db1.authenticate('shivam','mama123')
                db1 = connection.stats
                self.cricket_teams = db1.cricket_teams
        

        def test_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[0].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.test_list.append(_dict)
                            #print {'team':x.findAll('td')[0].string}
                        except:
                            pass
                self.cricket_stats.update({"format":"Test"},{"$set":{'ranking':self.test_list}},upsert=True)
                pprint.pprint(self.test_list)
                print
        

        def odi_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[1].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.odi_list.append(_dict)
                            self.cricket_teams.update({'team':x.findAll('td')[0].string},{'$set':{'team':x.findAll('td')[0].string,'league_id':'','season':'','team_id':'','flag_image':''}},upsert = True)
                        except:
                            pass
                self.cricket_stats.update({"format":"Odi"},{"$set":{'ranking':self.odi_list}},upsert=True)
                pprint.pprint(self.odi_list)
                print
                                
        def t20_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[2].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.t20_list.append(_dict)
                        except:
                            pass
                self.cricket_stats.update({"format":"T20"},{"$set":{'ranking':self.t20_list}},upsert=True)
                pprint.pprint(self.t20_list)




def main():
        obj = CricketRanking()
        obj.test_ranking()
        obj.odi_ranking()
        obj.t20_ranking()

if __name__=='__main__':main()


