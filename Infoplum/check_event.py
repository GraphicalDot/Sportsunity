#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
import pymongo
from pprint import pprint
from termcolor import cprint
from pyfiglet import figlet_format
import hashlib
from send_notification import NotifyEvent

class Infoplum_event:

        def __init__(self):

                self.sent = []
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_notifications = db.test_notifications
                self.obj = NotifyEvent()

        def get_scorecard_soup(self,series_id,match_id,comment):
        
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
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                 "http://schema.sportsflash.com.au/Cricket/GetFullScorecard"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                scorecard_soup = BeautifulSoup((r.content),'lxml')
                print '::::::'*2,self.sent
                self.notification = {}
                self.check_match_event(scorecard_soup,comment,series_id,match_id)
                from IPython import embed
                embed()
		if self.notification:
			print self.notification
                        #self.obj.send_notification(self.notification)
                

        def check_match_event(self,scorecard_soup,comment,series_id,match_id):


                if scorecard_soup.find('manofmatch').text:
                    if not self.test_notifications.find_one({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('manofmatch').text).hexdigest()}):
                        self.notify('MoM!',scorecard_soup.find('manofmatch').text,'',match_id,series_id)
                        self.test_notifications.update({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('manofmatch').text).hexdigest()},\
                                {'$set':{'match_id':match_id,'series_id':series_id,'commentary_id':\
                                hashlib.md5(scorecard_soup.find('manofmatch').text).hexdigest()}},upsert=True)

                if scorecard_soup.find('result').text:
                    if not self.test_notifications.find_one({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('result').text).hexdigest()}):
                        self.notify('Result!',scorecard_soup.find('result').text,'',match_id,series_id)
                        self.test_notifications.update({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('result').text).hexdigest()},\
                                {'$set':{'match_id':match_id,'series_id':series_id,'commentary_id':\
                                hashlib.md5(scorecard_soup.find('result').text).hexdigest()}},upsert=True)


                if scorecard_soup.find('toss').text:
                    if not self.test_notifications.find_one({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('toss').text).hexdigest()}):
                        self.notify('TOSS!',scorecard_soup.find('toss').text,'',match_id,series_id)
                        self.test_notifications.update({'match_id':match_id,'commentary_id':hashlib.md5(scorecard_soup.find('toss').text).hexdigest()},\
                            {'$set':{'match_id':match_id,'series_id':series_id,'commentary_id':\
                            hashlib.md5(scorecard_soup.find('toss').text).hexdigest()}},upsert=True)

                if comment.get('howoutid')!='0' and comment.get('howoutid'):
                    if 'Over ' in comment.find('comment').text:
                        self.notify('WICKET!',comment.find('comment').text,comment.get('boundarytype'),match_id,series_id)
                if comment.get('boundarytype') == '' or comment.get('boundarytype') == '0':
                    pass
                else:
                    print 'Over ' in comment.find('comment').text
                    if 'Over ' in comment.find('comment').text:
                        self.notify('BOUNDARY!',comment.find('comment').text,comment.get('boundarytype'),match_id,series_id)
                self.check_milestone(comment.get('batsmanid'),scorecard_soup,comment,match_id,series_id)
                self.check_milestone(comment.get('nonfacingbatsmanid'),scorecard_soup,comment,match_id,series_id)
                return 

        def notify(self,event,comment,boundary,match_id,series_id):
                self.event = event
                self.comment = comment
                cprint(figlet_format(event, font='starwars'), attrs=['bold'])
                print comment
                cprint(figlet_format(boundary, font='starwars'), attrs=['bold'])
                print '-'*10
                try:
                    self.notification.update({'t1':self.comment.split(': ')[0]+self.comment.split(': ')[1].split(',',2)[1],'t2':\
                            self.comment.split(': ')[1].split(',',2)[0],'e':self.event,'mid':match_id,'sid':1})
                except Exception,e:
                    self.notification.update({'t1':self.event,'t2':self.comment,'e':self.event,'mid':match_id,'sid':1})
                    print self.notification
                    from IPython import embed
                    embed()
                return 

        def check_milestone(self,player_id,scorecard_soup,comment,match_id,series_id):
                self.comment = comment.find('comment').text
                #batsmen = scorecard_soup.findAll('batsman')
                try:
                    if int(scorecard_soup.find('batsman',{'batsmanid':player_id}).find('run').text)>=int(50) and player_id not in self.sent:
                        print player_id*10
                        self.sent.append(player_id)
                        self.event = 'Milestone'
                        self.notification.update({'event_comment':self.comment,'e':self.event,'mid':match_id,'sid':1})
                except Exception,e:
                    pass
                return



if __name__=="__main__":

        obj = Infoplum_data_commentary()
        obj.get_match_list()
