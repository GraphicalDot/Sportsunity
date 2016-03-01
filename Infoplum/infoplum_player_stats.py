#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pymongo

class Infoplum_data:


        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_players = db.test_infoplum_players

        def get_teams_list(self):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>
    <GetTeamList xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <localeId>en</localeId>
      <matchTypeId>2</matchTypeId>
    </GetTeamList>
  </soap:Body>
</soap:Envelope>"""

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetTeamList"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')

                for team in soup.findAll('team'):
                        print team 
                        print 
                        self.get_player_list(team.get('teamid'),team.find('longname').text,team.find('shortname').text)

                        #self.test_infoplum_players.update({'team_id':team.get('teamid'),'team_name':team.find('longname').text},{'$set':{'team_id':team.get('teamid'),'team_name':\
                                #team.find('longname').text,'team_name_short':team.find('shortname').text,}},upsert=True)



        def get_player_list(self,team_id,team_name,team_short_name):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>
    <GetPlayerList xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <teamId>{0}</teamId>
    </GetPlayerList>
  </soap:Body>
</soap:Envelope>""".format(team_id)

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetPlayerList"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                #self.info = []

                for player in soup.findAll('player'):
                        print player  
                        print 
                        debut = player.find('debut')
                        info = {'birth_place':player.find('birthplace').text,'full_name':player.find('fullname').text,'born':player.find('dob').text,'batting_style':player.find('battingstyle').text,'bowling_style':\
                                player.find('bowlingstyle').text,'debut_date':debut.find('date').text,'debut_series':debut.find('series').text}

                        self.get_player_stats(player.get('playerid'))

                        print self.stats_dict

                        self.test_infoplum_players.update({'player_id':player.get('playerid'),'team_id':team_id},{'$set':{'player_id':player.get('playerid'),'name':player.find('fullname').text,'team':team_name,'team_id':\
                                team_id,'player_image':player.get('imageurl'),'info':info,'statistics':self.stats_dict}},upsert=True)



        
        def get_player_stats(self,player_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>
    <GetPlayerStats xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <playerId>{0}</playerId>
      <teamPlayedForId>0</teamPlayedForId>
      <teamPlayedAgainstId>0</teamPlayedAgainstId>
    </GetPlayerStats>
  </soap:Body>
</soap:Envelope>""".format(player_id)


                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetPlayerStats"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                self.stats_dict = {}

            
                try:
                    career_stats = soup.findAll('careerstats')[0]
                    for stat in career_stats.findAll('matchtype'):
                        batsman = stat.find('batting')
                        bowler = stat.find('bowling')
                        self.stats_dict.setdefault(stat.find('matchtypename').text.replace('.',''),{}).setdefault('batting',{}).update({'matches':stat.find('matches').text,'innings':batsman.find('innings').text,'runs':\
                                batsman.find('runs').text,'50s':batsman.find('fifties').text,'100s':batsman.find('centuries').text})
                        self.stats_dict.setdefault(stat.find('matchtypename').text.replace('.',''),{}).setdefault('bowling',{}).update({'matches':stat.find('matches').text,'innings':bowler.find('innings').text,'wickets':\
                                bowler.find('wickets').text,'overs':bowler.find('overs').text,'economy':bowler.find('economyrate').text})
                except:
                    pass

                return


if __name__=="__main__":

        obj = Infoplum_data()
        obj.get_teams_list()
