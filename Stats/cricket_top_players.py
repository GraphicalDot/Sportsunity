#!usr/bin/env python


import requests
from bs4 import BeautifulSoup
import pymongo

class TopCricketPlayers:

    def __init__(self,link):

        self.link = link
        response = requests.get(self.link)
        self.soup = BeautifulSoup(response.content,'lxml')
        conn = pymongo.MongoClient()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.cricket
        self.top_cricket_players = db.top_cricket_players


    def get_players(self):

        table = self.soup.findAll("table", {"class":"StoryengineTable"})
        body = table[0].findAll("tbody")
        column=body[0].findAll("td")[2]
        names=column.findAll("a",{"class":"mblLinkTxt"})

        for name in names:
            self.top_cricket_players.insert({'name':name.text})
        print 'stored'


def main():
    obj = TopCricketPlayers('http://www.espncricinfo.com/ci/content/rss/feeds_rss_cricket.html')
    obj.get_players()


if __name__ == '__main__':main()


            
