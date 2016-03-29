#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class AllPlayers:

    def __init__(self,url):
        response = requests.get(url)
        self.soup = BeautifulSoup(response.content)
        conn = connection.get_mongo_connection()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.stats
        self.cricket_players = db.cricket_players


    def getplayers(self):
        data=self.soup.find('div',{'id':'mw-content-text'})
        all_players=data.findAll('p')
        for team,player in zip(data.findAll('span',{'class':'mw-headline'}),all_players[3:28]):
            names = player.findAll('a')
            print team.text
            for name in names:
                self.cricket_players.insert({'team_id':team.text,'name':name.text,'yellow_cards':'','league_id':'','age':'','goals':'','position':'','nationality':team.text,'red_cards':'','jersey':''})
            print


def main():
    obj = AllPlayers('https://en.wikipedia.org/wiki/List_of_One_Day_International_cricketers')
    obj.getplayers()



if __name__=="__main__":main()

