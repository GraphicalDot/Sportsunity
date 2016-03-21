#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import json
import pymongo
import hashlib
import pprint

class CricketPlayerStats():

    def __init__(self,team):
        self.team = team
        conn = pymongo.MongoClient()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.test
        self.player_stats = db.player_stats


    def get_links(self):
        url = 'http://www.thatscricket.com/{0}/players/'.format(self.team)
        res = requests.get(url)
        soup = BeautifulSoup(res.content)
        print soup.findAll('div',{'id':'all'})
        all_data = soup.findAll('div',{'id':'all'})
        for player in all_data[0].findAll('li'):
            link=player.find('a')
            self.get_stats('http://www.thatscricket.com/'+str(link.get('href')))

    def get_stats(self,link):
        dict1 = {}
        stats_list = []
        response = requests.get(link)
        soup=BeautifulSoup(response.content)
        try:
            table=soup.findAll('div',{'id':'cricket-battingPerformaceBlock'})[0]
            w=table.findAll('tr')
            full_name=soup.find('div',{'class':'cricket-profileText'})
            print full_name.text
            print 
            description = soup.find('div',{'class':'cricket-profileDesc'})
            profile = description.findAll('div',{'class':'cricket-profileDescTable'})
            profile_photo=soup.findAll('div',{'class':'cricket-profilePhoto'})
            for num in range(1,5):
                try:
                    q=w[num].findAll('td')
                    if q[0].text == 'ODI' or q[0].text == 'Tests' or q[0].text == 'Twenty20' or q[0].text.strip() == 'IPL':
                        #stats_list.append({'format':q[0].text.strip(),'matches':int(q[1].text),'innings':int(q[2].text),'N.O':q[3].text,'runs':q[4].text,'highest':q[5].text,'average':\
                                #q[6].text,'strike_rate':q[7].text,'100s':q[8].text,'type':'batting'})
                        dict1.setdefault('batting',[]).append({'format':q[0].text.strip(),'matches':int(q[1].text),'innings':int(q[2].text),'not_out':q[3].text,'runs':q[4].text,'highest':q[5].text,'average':\
                                q[6].text,'strike_rate':q[7].text,'100s':q[8].text})
                        #self.player_stats.update('player':full_name.text,'player_id':hashlib.md5(full_name.text).hexdigest(),'stats':
                except Exception,e:
                    pass
        except Exception,e:
            profile = None

        try:

            table=soup.findAll('div',{'id':'cricket-battingPerformaceBlock'})[1]
            w=table.findAll('tr')
            for num in range(1,5):
                try:
                    q=w[num].findAll('td')
                    if q[0].text == 'ODI' or q[0].text == 'Tests' or q[0].text == 'Twenty20' or q[0].text.strip() == 'IPL':
                        #stats_list.append({'format':q[0].text.strip(),'matches':q[1].text,'balls':q[2].text,'runs':q[3].text,'wickets':q[4].text,'best':q[5].text,'average':\
                                #q[6].text,'economy':q[7].text,'type':'bowling'})
                        dict1.setdefault('bowling',[]).append({'format':q[0].text.strip(),'matches':q[1].text,'balls':q[2].text,'runs':q[3].text,'wickets':q[4].text,'best':q[5].text,'average':\
                                q[6].text,'economy':q[7].text})
                except Exception,e:
                    pass

            #dict1.update({'info':{'born':profile[1].text,'batting_style':profile[2].text.strip(),'place_of_birth':profile[4].text}})


        except Exception,e:
            pass


        #if profile:
        try:
            info = {}
            for heading,value in zip(profile[0].findAll('div',{'class':'cricket-profileTextBold'}),profile[0].findAll('div',{'class':'cricket-profileText'})):
                info[heading.text.replace(':','')] = value.text.strip()
            #info = {'born':profile[1].text,'batting_style':profile[2].text.strip(),'bowling_style':profile[3].text.strip(),'place_of_birth':profile[4].text}
        except Exception,e:
            #info = {'born':profile[1].text,'batting_style':profile[2].text.strip(),'place_of_birth':profile[3].text}
            info = None
        #else:
            #info = ''
        
        if soup.find('div',{'id':'cricket-battingPerformaceBlock'}):
        #if soup.find('div',{'id':'cricket-battingPerformaceBlock'}): 
            try:
                self.player_stats.update({'player_id':hashlib.md5(full_name.text).hexdigest(),'team_name':" ".join(self.team.split('-')).title()},{'$set':{'name':full_name.text,'player_id':\
                        hashlib.md5(full_name.text).hexdigest(),'stats':[dict1],'player_image':profile_photo[0].find('img').get('src'),'team_id':\
                        hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'info':info}},upsert=True)
            except Exception,e:
                self.player_stats.update({'player_id':hashlib.md5(full_name.text).hexdigest(),'team_name':" ".join(self.team.split('-')).title()},{'$set':{'name':full_name.text,'player_id':\
                        hashlib.md5(full_name.text).hexdigest(),'stats':[dict1],'player_image':'','team_id':hashlib.md5(" ".join(self.team.split('-')).title()).hexdigest(),'info':info}},upsert=True)
        else:
            print link
        

def main():
    teams = ['australia','new-zealand','india','south-africa','sri-lanka','pakistan','west-indies','bangladesh','ireland','afghanistan','zimbabwe','royal-challengers-bangalore','delhi-daredevils',\
            'chennai-super-kings','rajasthan-royals','kings-xi-punjab','mumbai-indians','kolkata-knight-riders','england']
    for team in teams:
        obj = CricketPlayerStats(team)
        obj.get_links()


if __name__=="__main__":main()
