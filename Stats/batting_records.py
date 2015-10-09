#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup




class BattingRecords:

        def __init__(self):
                response = requests.get('http://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;team=6;template=results;type=batting')
                self.soup = BeautifulSoup(response.content,"lxml")
                self.stats_list = list()
        
        def batting_cricket(self):
                for data in self.soup.find_all('table',{'class':'engineTable'}):
                        try:
                            body=data.find_all('tbody')
                            for stats in body:
                                rows = stats.find_all('tr')
                        except:
                            pass
            

                for row in rows:
                        stat=row.find_all('td')
                        _dict ={'player':stat[0].string,'span':stat[1].string,'match':stat[2].string,'inngs':\
                                stat[3].string,'notouts':stat[4].string,'runs':int(stat[5].string),'highst':stat[6].string}
                        self.stats_list.append(_dict)
                
                print self.stats_list


if __name__=='__main__':
        obj = BattingRecords()
        obj.batting_cricket()
