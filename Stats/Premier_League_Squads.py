#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import termcolor


class Squads:
        
        def __init__(self,link,team):
                res = requests.get(link)
                self.soup = BeautifulSoup(res.content,"lxml")
                self.team = team
                
        def get_squads(self):
                for s in self.soup.find_all('table',{'class':'contentTable'}):
                        rows=s.find_all('tr')
                        break

                print termcolor.colored(self.team.upper(),"red")
                print 
                for row in rows:
                        squad=row.find_all('td')
                        try:
                            print 'Jersey : '+squad[0].text.split('.')[0].strip(),'Name : '+squad[0].text.split('.')[1].strip(),'Position : '\
					    +squad[1].string, 'Nationality: '+squad[2].find('img').get('title')
                            print 'Played : '+squad[4].string,'Goals : '+squad[5].string,'Yellow : '+squad[6].string,'Red : '+squad[7].string
                            print 'Status : '+squad[8].text
                        except:
                            pass

def main():
        list_of_teams = ['arsenal','aston-villa','bournemouth','chelsea','man-utd','man-city','crystal-palace','everton','leicester','liverpool',\
                'newcastle','norwich','southampton','stoke','sunderland','swansea','spurs','watford','west-brom','west-ham']
        for team in list_of_teams:
            obj = Squads('http://www.premierleague.com/en-gb/clubs/profile.squads.html/'+str(team),team)
            obj.get_squads()


if __name__=='__main__':main()
