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
                        #dict1.setdefault(match.get('seriesid'),[]).append({'fixtures':self.list_of_fixtures})
                        self.test_infoplum_matches.update({'match_id':match.get('matchid'),'series_id':match.get('seriesid')},{'$set':{'match_id':match.get('matchid'),'match_name':match.get('matchname'),'series_id':\
                                match.get('seriesid'),'series_name':match.get('seriesname'),'start_date':match.find('datetime').text,'scorecard':self.scorecard}},upsert=True)
                         #   series.find('startdate').text,'end_date':series.find('enddate').text,'result':series.find('result').text,'fixtures':self.list_of_fixtures}},upsert=True)

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

                for inning in soup.findAll('inning'):
                        print inning
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

                        self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).update({'runs':inning.find('run').text,'overs':inning.find('over').text,'extra':\
                                inning.find('extra').text,'bye':inning.find('bye').text,'legbye':inning.find('legbye').text,'wide':inning.find('wide').text,'noball':inning.find('noball').text,'run_rate':\
                                inning.find('runrate').text,'required_runrate':inning.find('requiredrunrate').text})
                print

                return


if __name__=="__main__":

        obj = Infoplum_data()
        obj.get_match_list()
