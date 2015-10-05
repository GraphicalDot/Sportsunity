#!/usr/bin/env python


from bs4 import BeautifulSoup
import requests
import pymongo
    

class CricketRanking:

        def __init__(self):
                res = requests.get('http://www.espncricinfo.com/rankings/content/page/211271.html')
                self.soup = BeautifulSoup(res.content,'lxml')
                self.test_list = list()
                self.odi_list = list()
                self.t20_list = list()
                connection = pymongo.MongoClient()
                db = connection.drake
                self.cricket_stats = db.cricket_stats
        
        """
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
        """

        def test_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[0].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.test_list.append(_dict)
                        except:
                            pass
                self.cricket_stats.update({"format":"Test"},{"$set":{'ranking':self.test_list}},upsert=True)
        

        def odi_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[1].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.odi_list.append(_dict)
                        except:
                            pass
                self.cricket_stats.update({"format":"Odi"},{"$set":{'ranking':self.odi_list}},upsert=True)

                                
        def t20_ranking(self):
                for x in self.soup.findAll('table',{'class':'StoryengineTable'})[2].findAll('tr'):
                        try:
                            _dict = {'team':x.findAll('td')[0].string,'matches':x.findAll('td')[1].string,'points':\
                                    x.findAll('td')[2].string,'rating':x.findAll('td')[3].string}
                            self.t20_list.append(_dict)
                        except:
                            pass
                self.cricket_stats.update({"format":"T20"},{"$set":{'ranking':self.t20_list}},upsert=True)





def main():
        obj = CricketRanking()
        obj.test_ranking()
        obj.odi_ranking()
        obj.t20_ranking()

if __name__=='__main__':main()


