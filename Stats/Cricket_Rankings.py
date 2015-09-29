#!/usr/bin/env python


from bs4 import BeautifulSoup
import requests



class CricketRanking:

        def __init__(self):
                res = requests.get('http://sports.mapsofindia.com/cricket/latest-icc-odi-team-rankings.html')
                self.soup = BeautifulSoup(res.content,'lxml')
                self.rank_list = list()
        
        def odi_ranking(self):
                for x in self.soup.find_all('table',{'class':'tableizer-table'}):
                        ranks = x.find_all('tr')

                for rank in ranks:
                        data=rank.find_all('td')
                        try:
                            self.rank_list.append({'rank':data[0].string, 'team':data[1].string, 'matches':data[2].string, 'points':\
                                    data[3].string, 'rating':data[4].string})
                        except:
                            pass
                
                print self.rank_list




def main():
        obj = CricketRanking()
        obj.odi_ranking()

if __name__=='__main__':main()


