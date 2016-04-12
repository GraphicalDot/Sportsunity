#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
from pprint import pprint
import pymongo
from dateutil.parser import parse
import pytz
from datetime import datetime
from check_event import Infoplum_event

class Infoplum_data_commentary:


        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_commentary = db.test_infoplum_commentary
                self.test_notifications = db.test_notifications

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

                for match in soup.findAll('match'):
                        print match 
                        print
                        start_datetime = match.find('datetime').text
                        timezone = pytz.timezone('Australia/ACT')
                        date = parse(start_datetime)
                        local_std = timezone.localize(date)
                        local_utc = local_std.astimezone(pytz.utc)
                        utc_date = local_utc.strftime('%Y-%m-%d')
                        print utc_date
                        utc_now=datetime.utcnow()
                        utc_now_date = utc_now.strftime('%Y-%m-%d')
                        print utc_now_date


                        if str(match.find('result').get('status')) in ['F']:
                        #if utc_date == utc_now_date:
                            self.get_match_commentary(match.get('seriesid'),match.get('matchid'))
                            self.test_infoplum_commentary.update({'match_id':match.get('matchid'),'series_id':match.get('seriesid')},{'$set':{'match_id':match.get('matchid'),'result':match.find('result').text,'match_name':\
                                    match.get('matchname'),'series_id':match.get('seriesid'),'series_name':match.get('seriesname'),'start_date':match.find('datetime').text,'commentary':\
                                    self.commentary,'status':match.find('result').get('status'),'home_team':match.find('hometeam').get('fullname'),'home_team_id':\
                                    match.find('hometeam').get('teamid'),'away_team':match.find('awayteam').get('fullname'),'away_team_id':match.find('awayteam').get('teamid')}},upsert=True)

                print


        
        def get_match_commentary(self,series_id,match_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
      <UserName>TUFETQ==</UserName>
      <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
    </AuthenticationHeader>
  </soap:Header>
  <soap:Body>
    <GetCommentary xmlns="http://schema.sportsflash.com.au/Cricket/">
      <clientId>209</clientId>
      <localeId>en</localeId>
      <seriesId>{0}</seriesId>
      <matchId>{1}</matchId>
      <inningId>1</inningId>
      <overLimit>0</overLimit>
    </GetCommentary>
  </soap:Body>
</soap:Envelope>""".format(series_id,match_id)

                print body

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetCommentary"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')

                self.commentary = []
                comment_ids = []

                obj = Infoplum_event()

                if soup.findAll('otherinning'):

                    for other_inning in soup.findAll('otherinning'):
                            body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
          <UserName>TUFETQ==</UserName>
          <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
        </AuthenticationHeader>
      </soap:Header>
      <soap:Body>
        <GetCommentary xmlns="http://schema.sportsflash.com.au/Cricket/">
          <clientId>209</clientId>
          <localeId>en</localeId>
          <seriesId>{0}</seriesId>
          <matchId>{1}</matchId>
          <inningId>{2}</inningId>
          <overLimit>0</overLimit>
        </GetCommentary>
      </soap:Body>
    </soap:Envelope>""".format(series_id,match_id,other_inning.get('inningid'))

                            print
                            print body

                            encoded_request = body.encode('utf-8')
                            headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetCommentary"}
                            r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                            print r.reason
                            soup = BeautifulSoup(r.content)
                            
                            for comment in soup.findAll('commentary'):
                                    if not self.test_notifications.find_one({'match_id':match_id,'commentary_id':comment.get('commentaryid')}):
                                        obj.get_scorecard_soup(series_id,match_id,comment)
                                        self.test_notifications.update({'match_id':match_id,'commentary_id':comment.get('commentaryid')},{'$set':{'match_id':match_id,'series_id':series_id,'commentary_id':\
                                                comment.get('commentaryid')}},upsert=True)

                                    #self.commentary.setdefault(other_inning.get('inningid'),[]).append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.get('datetimelabel'),'how_out':\
                                            #comment.get('howoutid'),'comment':comment.find('comment').text})
                                    self.commentary.append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.find('datetimelabel').text,'how_out':comment.get('howoutid'),'comment':\
                                            comment.find('comment').text,'commentary_datetime_utc':comment.find('datetimeutc').text,'inning_id':str(other_inning.get('inningid'))})

                else:
                    body = """<?xml version="1.0" encoding="utf-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
      <soap:Header>
        <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
          <UserName>TUFETQ==</UserName>
          <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
        </AuthenticationHeader>
      </soap:Header>
      <soap:Body>
        <GetCommentary xmlns="http://schema.sportsflash.com.au/Cricket/">
          <clientId>209</clientId>
          <localeId>en</localeId>
          <seriesId>{0}</seriesId>
          <matchId>{1}</matchId>
          <inningId>0</inningId>
          <overLimit>0</overLimit>
        </GetCommentary>
      </soap:Body>
    </soap:Envelope>""".format(series_id,match_id)

                    encoded_request = body.encode('utf-8')
                    headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetCommentary"}
                    r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                    print r.reason
                    soup = BeautifulSoup(r.content)
                    
                    for comment in soup.findAll('commentary'):
                            if comment.get('commentaryid') not in comment_ids:
                                obj.get_scorecard_soup(series_id,match_id,comment)

                            #self.commentary.setdefault(other_inning.get('inningid'),[]).append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.get('datetimelabel'),'how_out':\
                                    #comment.get('howoutid'),'comment':comment.find('comment').text})
                            self.commentary.append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.find('datetimelabel').text,'how_out':comment.get('howoutid'),'comment':\
                                    comment.find('comment').text,'commentary_datetime_utc':comment.find('datetimeutc').text,'inning_id':'1'})  

                    print self.commentary
                return



if __name__=="__main__":

        obj = Infoplum_data_commentary()
        obj.get_match_list()
