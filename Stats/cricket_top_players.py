#!usr/bin/env python

import requests
from bs4 import BeautifulSoup
import hashlib
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class TopCricketPlayers:

    def __init__(self,link):

        self.link = link
        response = requests.get(self.link)
        self.soup = BeautifulSoup(response.content,'lxml')
        conn = connection.get_mongo_connection()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.cricket
        self.top_cricket_players = db.top_cricket_players


    def get_players(self):

        """
        table = self.soup.findAll("table", {"class":"StoryengineTable"})
        body = table[0].findAll("tbody")
        column=body[0].findAll("td")[2]
        names=column.findAll("a",{"class":"mblLinkTxt"})

        for name in names:
            print name.text
            self.top_cricket_players.insert({'name':name.text})
        print 'stored'

        """

        table = self.soup.findAll('table',{'class':'cricket-allRecordsTable'})

        for player in table[1].findAll('tr'):
            try:

                link = player.findAll('a')[1].get('href')
                res = requests.get('http://www.thatscricket.com/'+link)
                soup = BeautifulSoup(res.content)
                #description = soup.find('div',{'class':'cricket-profileDesc'})
                full_name=soup.find('div',{'class':'cricket-profileText'})
                self.top_cricket_players.update({'player_id':hashlib.md5(full_name.text).hexdigest()},{'$set':{'name':full_name.text,'player_id':hashlib.md5(full_name.text).hexdigest()}},upsert=True)
                print full_name.text

            except Exception,e:
                pass

        """
        for player in table[1].findAll('tr'):
            try:
                self.top_cricket_players.insert({'name':player.findAll('a')[1].text})
            except Exception,e:
                pass
        """
        
def main():
    #obj = TopCricketPlayers('http://www.espncricinfo.com/ci/content/rss/feeds_rss_cricket.html')
    obj = TopCricketPlayers('http://www.thatscricket.com/statistics/')
    obj.get_players()


if __name__ == '__main__':main()


            
