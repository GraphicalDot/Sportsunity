#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class BigBash:

    def __init__(self,url):

        response = requests.get(url)
        self.soup = BeautifulSoup(response.content,"lxml")
        conn = connection.get_mongo_connection()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.stats
        self.cricket_teams = db.cricket_teams



    def get_teams(self):

        table=self.soup.find('table',{'class':'wikitable'})
        for team in table.findAll('tr'):
            try:
                self.cricket_teams.update({'team_name':team.find('a').text},{'$set':{'team_name':team.find('a').text,'league_id':'','season':'','flag_image':'','team_id':'','type':'Indian_premier_league'}},upsert=True)
                #print {'team_name':team.find('a').text,'league_id':'','season':'','flag_image':'','team_id':'','type':'Indian_premier_league'}
            except Exception,e:
                pass



def main():
    obj = BigBash("https://en.wikipedia.org/wiki/Indian_Premier_League")
    #obj = BigBash('https://en.wikipedia.org/wiki/List_of_International_Cricket_Council_members')
    obj.get_teams()


if __name__=="__main__":main()
