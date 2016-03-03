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
                self.test_infoplum_commentary = db.test_infoplum_commentary

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
                        self.get_match_commentary(match.get('seriesid'),match.get('matchid'))
                        #dict1.setdefault(match.get('seriesid'),[]).append({'fixtures':self.list_of_fixtures})
                        self.test_infoplum_commentary.update({'match_id':match.get('matchid'),'series_id':match.get('seriesid')},{'$set':{'match_id':match.get('matchid'),'match_name':match.get('matchname'),'series_id':\
                                match.get('seriesid'),'series_name':match.get('seriesname'),'start_date':match.find('datetime').text,'commentary':self.commentary}},upsert=True)
                         #   series.find('startdate').text,'end_date':series.find('enddate').text,'result':series.find('result').text,'fixtures':self.list_of_fixtures}},upsert=True)

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
                                #self.commentary.setdefault(other_inning.get('inningid'),[]).append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.get('datetimelabel'),'how_out':\
                                        #comment.get('howoutid'),'comment':comment.find('comment').text})
                                self.commentary.append({'commentary_id':comment.get('commentaryid'),'commentary_datetime':comment.get('datetimelabel'),'how_out':comment.get('howoutid'),'comment':\
                                        comment.find('comment').text,'inning_id':str(other_inning.get('inningid'))})

                        print self.commentary
                #return



if __name__=="__main__":

        obj = Infoplum_data()
        obj.get_match_list()
