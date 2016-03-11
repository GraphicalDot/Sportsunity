#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pymongo

class Infoplum_data_series:


        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum = db.test_infoplum

        def get_series_list(self):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>
    <GetFullSeriesList xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
    </GetFullSeriesList>
  </soap:Body>
</soap:Envelope>"""

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetFullSeriesList"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                #dict1 = {}

                for series in soup.findAll('series'):
                        print series 
                        print 
                        # dict1.setdefault(series.get('seriesid'),[]).append({'series_id':series.get('seriestypename'),'series_name':series.find('name').text,'start_date':series.find('startdate').text,'end_date':series.find('enddate').text,'result':series.find('result').text})
                        self.get_series_fixtures(series.get('seriesid'))
                        self.get_points_table(series.get('seriesid'))
                        # dict1.setdefault(series.get('seriesid'),[]).append({'fixtures':self.list_of_fixtures})
                        self.test_infoplum.update({'series_id':series.get('seriesid')},{'$set':{'series_id':series.get('seriesid'),'series_type':series.get('seriestypename'),'series_name':series.find('name').text,'start_date':\
                            series.find('startdate').text,'end_date':series.find('enddate').text,'result':series.find('result').text,'fixtures':\
                            self.list_of_fixtures,'season_table':self.season_table}},upsert=True)

                print



        def get_series_fixtures(self,series_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>  
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>    
    <GetFixture xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <seriesId>{0}</seriesId>
    </GetFixture>
  </soap:Body>   
</soap:Envelope>""".format(series_id)
  
                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetFixture"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                self.list_of_fixtures = []

                for match in soup.findAll('match'):
                        print match
                        print
                        #dict2.setdefault(match.find('name').text,[]).append({'match_id':match.get('matchid'),'series_id':match.get('seriesid'),'start_date':match.find('datestart').text,'end_date':match.find('dateend').text,'venue':\
                                #match.find('venue1').text,'result':match.find('result').text})
                        self.list_of_fixtures.append({'match_name':match.find('name').text,'match_id':match.get('matchid'),'start_date':match.find('datestart').text,'end_date':match.find('dateend').text,'venue':\
                                match.find('venue1').text,'match_time':match.find('startdatetimeutc').text,'result':match.find('result').text})

                print

                return


        def get_points_table(self,series_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>  
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>    
    <GetStandings xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <seriesId>{0}</seriesId>
    </GetStandings>
  </soap:Body>   
</soap:Envelope>""".format(series_id)
  
                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetStandings"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                table = []
                self.season_table = {}

                for team in soup.findAll('team'):
                        print team
                        print 
                        table.append({'group_id':team.get('groupid'),'group_name':team.get('groupname'),'team_name':team.find('name').text,'team_id':\
                            team.get('teamid'),'played':team.find('played').text,'points':team.find('points').text,'won':team.find('won').text,'lost':\
                            team.find('lost').text,'net_run_rate':team.find('netrunrate').text,'tied':team.find('tied').text})

                for group in table:
                        self.season_table.setdefault(group['group_name'],[]).append(group)

                return



if __name__=="__main__":

        obj = Infoplum_data_series()
        obj.get_series_list()

        
