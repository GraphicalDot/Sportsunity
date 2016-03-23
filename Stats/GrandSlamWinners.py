import os
import sys
from bs4 import BeautifulSoup
import requests
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


class GrandSlams:

        def __init__(self, link):
                self.columns = list()
                conn = connection.get_mongo_connection()
                db = conn.drake
                self.tennis_stats = db.tennis_stats
                res = requests.get(link)
                self.soup = BeautifulSoup(res.content,'lxml')
        
        @profile
        def men(self):
                for table in self.soup.findAll('table',{'class':'tablehead'}):
                        all_rows = table.findAll('tr')


                #self.columns = [(row.findAll('td')) for row in all_rows]

                for row in all_rows:
                        self.columns.append(row.findAll('td'))
                        
                for column in self.columns:
                        if len(column)>2 :
                                if not column[0].text=="YEAR":
                                        self.tennis_stats.update({'Category':'Men','Year':column[0].text},{'$set':{'Category':'Men','Year':\
                                                column[0].text,'Tournament':column[1].text,'Winner':column[2].text,'Runner_Up':\
                                                column[3].text}}, upsert = True)
                        else:
                                pass
        @profile
        def women(self):
                for table in self.soup.findAll('table',{'class':'tablehead'}):
                        all_rows = table.findAll('tr')

                for row in all_rows:
                        self.columns.append(row.findAll('td'))

                for column in self.columns:
                        if len(column)>2 :
                                if not column[0].text=="YEAR":
                                        self.tennis_stats.update({'Category':'Women','Year':column[0].text},{'$set':{'Category':'Women','Year':\
                                            column[0].text,'Tournament':column[1].text,'Winner':column[2].text,'Runner_Up':\
                                            column[3].text}}, upsert = True)
                        else:
                                pass



if __name__=="__main__":
        obj = GrandSlams('http://sports.espn.go.com/sports/tennis/history?type=men')
        obj.men()
        obj1 = GrandSlams('http://sports.espn.go.com/sports/tennis/history?type=women')
        obj1.women()





