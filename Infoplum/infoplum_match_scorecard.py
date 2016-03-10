#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pymongo

class Infoplum_data_scorecard:


        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_matches = db.test_infoplum_matches

        def get_match_list(self):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetMatchList xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                </GetMatchList>
                </soap:Body>
                </soap:Envelope>"""

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetMatchList"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                #dict1 = {}

                for match in soup.findAll('match'):
                        print match 
                        print 
                        # dict1.setdefault(series.get('seriesid'),[]).append({'series_id':series.get('seriestypename'),'series_name':series.find('name').text,'start_date':series.find('startdate').text,'end_date':series.find('enddate').text,'result':series.find('result').text})
                        self.get_match_scorecard(match.get('seriesid'),match.get('matchid'))

                        self.match_summary(match.get('seriesid'),match.get('matchid'),self.upcoming_batsmen)

                        #dict1.setdefault(match.get('seriesid'),[]).append({'fixtures':self.list_of_fixtures})
			self.test_infoplum_matches.update({'match_id':match.get('matchid'),'series_id':match.get('seriesid')},{'$set':{'match_id':match.get('matchid'),'result':match.find('result').text,'match_name':\
				match.get('matchname'),'series_id':match.get('seriesid'),'series_name':match.get('seriesname'),'start_date':match.find('datetime').text,'scorecard':\
                                self.scorecard,'status':match.find('result').get('status'),'home_team':match.find('hometeam').get('fullname'),'home_team_id':\
                                match.find('hometeam').get('teamid'),'summary':self.summary,'away_team':match.find('awayteam').get('fullname'),'away_team_id':match.find('awayteam').get('teamid')}},upsert=True)

                print


        
        def get_match_scorecard(self,series_id,match_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetFullScorecard xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                <localeId>en</localeId>
                <seriesId>{0}</seriesId>
                <matchId>{1}</matchId>
                </GetFullScorecard>
                </soap:Body>
                </soap:Envelope>""".format(series_id,match_id)
   
                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetFullScorecard"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                print soup.prettify()
                self.scorecard = {}
                playing_xi = {}
                self.upcoming_batsmen = {}

                for inning in soup.findAll('inning'):
                        print
                        for batsman in inning.findAll('batsman'):
                                self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('batting',[]).append({'batsman_id':batsman.get('batsmanid'),\
                                        'batsman_name':batsman.find('name').text,'runs':batsman.find('run').text,'balls':batsman.find('ball').text,'strike_rate':batsman.find('strikerate').text,\
                                        'how_out':batsman.find('howout').text,'six':batsman.find('six').text,'four':batsman.find('four').text})

                        #self.list_of_fixtures.append({'match_name':match.find('name').text,'match_id':match.get('matchid'),'start_date':match.find('datestart').text,'end_date':match.find('dateend').text,'venue':\
                                #match.find('venue1').text,'result':match.find('result').text})

                        for bowler in inning.findAll('bowler'):
                                print bowler
                                try:
                                        self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('bowling',[]).append({'bowler_name':bowler.find('name').text,\
                                                'bowler_id':bowler.get('bowlerid'),'runs':bowler.find('run').text,'overs':bowler.find('over').text,'maidens':bowler.find('maiden').text,'wickets':bowler.find('wicket').text,'economy':\
                                                bowler.find('economy').text,'strike_rate':bowler.find('strikerate').text})
                                except Exception,e:
                                        pass
                        
                        """
                        getting fall_of_wickets and did_not_bat
                        """

                        batsmen = inning.findAll('batsman')
                        for batsman in batsmen:
                                playing_xi.setdefault(inning.find('name').text,[]).append({'player':batsman.find('name').text,'fow':batsman.get('foworder'),'runs':batsman.find('run').text,'comment':\
                                    batsman.find('wktcommentary').text})

                        for player in playing_xi[inning.find('name').text]:
                                if player['fow']:
                                    self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('fall_of_wickets',[]).append({'name':\
                                        player['player'],'fow_order':player['fow'],'runs':player['runs']})
                                elif not player['runs']:
                                    self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('did_not_bat',[]).append({'name':\
                                        player['player']})
                                    self.upcoming_batsmen.setdefault(inning.get('inningid'),[]).append({'name':player['player']})

                        """
                        getting extras
                        """

                        self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).update({'runs':inning.find('run').text,'overs':inning.find('over').text,'extra':\
                                inning.find('extra').text,'bye':inning.find('bye').text,'legbye':inning.find('legbye').text,'wide':inning.find('wide').text,'noball':inning.find('noball').text,'run_rate':\
                                inning.find('runrate').text,'required_runrate':inning.find('requiredrunrate').text})
                print

                return


        def match_summary(self,series_id,match_id,upcoming_batsmen):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetScorecard xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                <localeId>en</localeId>
                <seriesId>{0}</seriesId>
                <matchId>{1}</matchId>
                </GetScorecard>
                </soap:Body>
                </soap:Envelope>""".format(series_id,match_id)

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetScorecard"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                print soup.prettify()

                self.summary = {}
                current_bowler = []
                recent_over = []

                for bowler in soup.findAll('bowler'):
                    if bowler.get('bowlertype') == 'CurrentBowler':
                        current_bowler.append({'player_id':bowler.get('playerid'),'name':bowler.find('name').text,'runs':bowler.find('run').text,'wicket':bowler.find('wicket').text,'overs':bowler.find('bowlerover').text})
                    else:
                        pass

                self.summary.update({'current_bowler':current_bowler})

                current_inning = soup.find('header').get('inningid')

                try:
                    print upcoming_batsmen
                    print
                    upcoming_batsmen = upcoming_batsmen[current_inning]
                except Exception,e:
                    print e

                try:
                    for over in soup.findAll('over')[-1]:
                        recent_over.append({'ball_id':over.get('balllegalno'),'wicket':over.get('hasdismissed'),'runs':over.find('run').text,'over':soup.findAll('over')[-1].get('overid')})
                except Exception,e:
                    print e 

                self.summary.update({'recent_over':recent_over,'upcoming_batsmen':upcoming_batsmen})

                return

                


if __name__=="__main__":

        obj = Infoplum_data_scorecard()
        obj.get_match_list()

