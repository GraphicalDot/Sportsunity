#!usr/bin/env python

import requests
from bs4 import BeautifulSoup


class TopFootballPlayers:


    def __init__(self,link):

        self.link = link
        self.response = requests.get(link)
    

    def get_players(self):

        soup = BeautifulSoup(self.response.content,'lxml')
        column = soup.find("div", {"id":"col1"})
        players = column.findAll('div',{'class':'i'})
        for player in players:
            print player.find('b').text



def main():
    obj = TopFootballPlayers('http://www.thetoptens.com/football-soccer-players-2015/')
    obj.get_players()

if __name__ == '__main__':
    main()
