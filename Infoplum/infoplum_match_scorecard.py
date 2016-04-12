#!/usr/bin/env python


import requests
from bs4 import BeautifulSoup
import json
from operator import itemgetter
from pprint import pprint
import pytz
from datetime import datetime
from dateutil.parser import parse
import calendar
import pymongo

class Infoplum_data_scorecard:


        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_matches = db.test_infoplum_matches
                self.infoplum_images = db.infoplum_images
                self.infoplum_team_flags = db.infoplum_team_flags

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
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                 "http://schema.sportsflash.com.au/Cricket/GetMatchList"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                #dict1 = {}

                for match in soup.findAll('match'):
                        print match 
                        print 

                        """
                        converting to GMT Timezone
                        """

                        match_type_id = soup.find('match').get('matchtypeid')
                        start_datetime = match.find('datetime').text
                        timezone = pytz.timezone('Australia/ACT')
                        date = parse(start_datetime)
                        local_std = timezone.localize(date)
                        local_utc = local_std.astimezone(pytz.utc)
                        time_tuple = datetime.timetuple(local_utc)
                        gmt_epoch = calendar.timegm(time_tuple)
                        utc_date = local_utc.strftime('%Y-%m-%d')

                        utc_now=datetime.utcnow()
                        utc_now_date = utc_now.strftime('%Y-%m-%d')

                        if utc_date == utc_now_date and match_type_id!='3':
                            self.get_match_details(match.get('seriesid'),match.get('matchid'))
                            self.get_match_scorecard(match.get('seriesid'),match.get('matchid'))
                            self.match_summary(match.get('seriesid'),match.get('matchid'),self.upcoming_batsmen,self.toss,self.umpires)


                        #dict1.setdefault(match.get('seriesid'),[]).append({'fixtures':self.list_of_fixtures})
                        try:
                            print self.match_status,'----'*10
                            self.test_infoplum_matches.update({'match_id':match.get('matchid'),'series_id':match.get('seriesid')},{'$set':{'match_id':match.get('matchid'),'result':match.find('result').text,'match_name':\
                                match.get('matchname'),'series_id':match.get('seriesid'),'series_name':match.get('seriesname'),'start_date':match.find('datetime').text,'match_time':gmt_epoch,'scorecard':\
                                self.scorecard,'status':self.match_status,'home_team':match.find('hometeam').get('fullname'),'match_widget':self.score_widget,'home_team_id':\
                                match.find('hometeam').get('teamid'),'home_team_flag':self.infoplum_team_flags.find_one({'team_id':match.find('hometeam').get('teamid')})['team_flag'],'summary':\
                                self.summary,'away_team':match.find('awayteam').get('fullname'),'away_team_id':match.find('awayteam').get('teamid'),'away_team_flag':\
                                self.infoplum_team_flags.find_one({'team_id':match.find('awayteam').get('teamid')})['team_flag']}},upsert=True)
                        except:
                            pass

                print


        def get_match_details(self,series_id,match_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetMatchDetails xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                <localeId>en</localeId>
                <seriesId>{0}</seriesId>
                <matchId>{1}</matchId>
                </GetMatchDetails>
                </soap:Body>
                </soap:Envelope>""".format(series_id,match_id)

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                        "http://schema.sportsflash.com.au/Cricket/GetMatchDetails"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')

                try:
                    self.match_status = soup.find('status').text
                    print '*'*10,self.match_status
                except Exception,e:
                    pass

                return


        
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
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                 "http://schema.sportsflash.com.au/Cricket/GetFullScorecard"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                print soup.prettify()
                self.scorecard = {}
                playing_xi = {}
                self.upcoming_batsmen = {}
                self.score_widget = list()

                for inning in soup.findAll('inning'):
                        print
                        for batsman in inning.findAll('batsman'):
                            if batsman.find('ball').text or batsman.find('run').text:
                                self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('batting',[]).append({'batsman_id':batsman.get('batsmanid'),\
                                        'batsman_name':batsman.find('name').text,'runs':batsman.find('run').text,'balls':batsman.find('ball').text,'strike_rate':batsman.find('strikerate').text,\
                                        'how_out':batsman.find('howout').text,'batsman_image':self.infoplum_images.find_one({'player_id':batsman.get('batsmanid')})['player_image'],'six':\
                                        batsman.find('six').text,'four':batsman.find('four').text})

                        #self.list_of_fixtures.append({'match_name':match.find('name').text,'match_id':match.get('matchid'),'start_date':match.find('datestart').text,'end_date':match.find('dateend').text,'venue':\
                                #match.find('venue1').text,'result':match.find('result').text})

                        print inning.findAll('bowler')
                        print '-'*10
                        for bowler in inning.findAll('bowler'):
                                print bowler
                                try:
                                    if bowler.get('position') or bowler.find('economy').text:
                                        self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('bowling',[]).append({'bowler_name':bowler.find('name').text,\
                                                'bowler_id':bowler.get('bowlerid'),'bowler_image':self.infoplum_images.find_one({'player_id':bowler.get('bowlerid')})['player_image'],'runs':\
                                                bowler.find('run').text,'overs':bowler.find('over').text,'maidens':bowler.find('maiden').text,'wickets':bowler.find('wicket').text,'economy':\
                                                bowler.find('economy').text,'strike_rate':bowler.find('strikerate').text})
                                except Exception,e:
                                    pass
                        
                        """
                        getting fall_of_wickets and did_not_bat
                        """

                        batsmen = inning.findAll('batsman')
                        for batsman in batsmen:
                            try:
                                playing_xi.setdefault(inning.find('name').text,[]).append({'player':batsman.find('name').text,'player_id':batsman.get('batsmanid'),'player_image':\
                                        self.infoplum_images.find_one({'player_id':batsman.get('batsmanid')})['player_image'],'fow':batsman.get('foworder'),'runs':batsman.find('run').text,'comment':\
                                        batsman.find('wktcommentary').text,'fow_over':batsman.find('fowover').text,'fow_score':batsman.find('fow').text})
                            except Exception,e:
                                playing_xi = []


                        if playing_xi:
                            for player in playing_xi[inning.find('name').text]:
                                if player['fow']:
                                    self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('fall_of_wickets',[]).append({'name':\
                                            player['player'],'fow_order':int(player['fow']),'fow_score':player['fow_score'],'fow_over':player['fow_over'],'runs':player['runs']})
                                    self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('fall_of_wickets',[]).sort(key=itemgetter('fow_order'))
                                elif not player['runs']:
                                    self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).setdefault('did_not_bat',[]).append({'name':\
                                        player['player']})
                                    self.upcoming_batsmen.setdefault(inning.get('inningid'),[]).append({'name':player['player'],'player_id':player['player_id'],'player_image':player['player_image']})

                        """
                        getting extras
                        """

                        self.scorecard.setdefault(inning.get('inningid'),{}).setdefault(inning.find('name').text,{}).update({'runs':inning.find('run').text,'overs':inning.find('over').text,'extra':\
                                inning.find('extra').text,'bye':inning.find('bye').text,'legbye':inning.find('legbye').text,'wide':inning.find('wide').text,'noball':inning.find('noball').text,'run_rate':\
                                inning.find('runrate').text,'required_runrate':inning.find('requiredrunrate').text})
                
                        
                        innings = inning.get('inningid')
                        try:
                            self.score_widget.append({'team_name':inning.find('team').text,'runs':inning.find('run').text,'overs':inning.find('over').text,'wickets':inning.find('wicket').text,'inning':innings})
                            print self.score_widget
                            print '-'*15
                        except Exception,e:
                            print e


                try:
                    self.toss = soup.find('toss').text
                except Exception,e:
                    self.toss = ''
                try:
                    self.umpires = {'first_umpire':soup.find('umpirefirst').text,'second_umpire':soup.find('umpiresecond').text,'third_umpire':soup.find('umpirethird').text,'referee':soup.find('referee').text}
                except Exception,e:
                    self.umpires = {}

                return



        def match_summary(self,series_id,match_id,upcoming_batsmen,toss,umpires):

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
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                 "http://schema.sportsflash.com.au/Cricket/GetScorecard"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')
                print '-'*20
                print soup.prettify()

                self.summary = {}
                #current_partnership = {}
                recent_over = []
                current_bowler = {}

                """
                current bowler
                """

                try:
                    for bowler in soup.findAll('bowler'):
                        if bowler.get('bowlertype') == 'CurrentBowler':
                        #current_bowler.append({'player_id':bowler.get('playerid'),'name':bowler.find('name').text,'runs':bowler.find('run').text,'wicket':bowler.find('wicket').text,'overs':bowler.find('bowlerover').text})
                            current_bowler = {'player_id':bowler.get('playerid'),'player_image':self.infoplum_images.find_one({'player_id':bowler.get('playerid')})['player_image'],'name':bowler.find('name').text,'runs':\
                                    bowler.find('run').text,'economy':float(bowler.find('economy').text),'wicket':bowler.find('wicket').text,'overs':bowler.find('bowlerover').text}
                except Exception,e:
                    print e
                    #current_bowler = {}

                self.summary.update({'current_bowler':current_bowler,'toss':toss,'umpires':umpires})

                """
                upcoming batsmen
                """

                current_inning = soup.find('header').get('inningid')

                try:
                    print upcoming_batsmen
                    print '--'*10
                    upcoming_batsmen = upcoming_batsmen[current_inning]
                except Exception,e:
                    upcoming_batsmen = []

                """
                recent over
                """

                try:
                    for over in soup.findAll('over')[-1]:
                        recent_over.append({'ball_id':over.get('balllegalno'),'wicket':over.get('hasdismissed'),'runs':over.find('run').text,'over':soup.findAll('over')[-1].get('overid')})
                except Exception,e:
                    print e 

                self.summary.update({'recent_over':recent_over,'upcoming_batsmen':upcoming_batsmen,'venue':soup.find('venue').text,'last_wicket':soup.find('lastwicket').text})

                """
                getting current partnership
                """

                self.get_current_partnership(match_id,series_id,current_inning)

                """
                getting man of the match
                """

                self.get_man_of_the_match(match_id,series_id)

                self.summary.update({'current_partnership':self.current_partnership,'man_of_the_match':self.man_of_the_match})

                """
                current partnership

                for batsman in soup.findAll('batsman'):
                    current_partnership.setdefault(batsman.get('batsmantype'),{}).update({'player_id':batsman.get('playerid'),'name':batsman.find('name').text})

                self.summary.update({'current_partnership':current_partnership})
                """

                return

        def get_current_partnership(self,match_id,series_id,current_inning):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetPartnership xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                <localeId>en</localeId>
                <seriesId>{1}</seriesId>
                <matchId>{0}</matchId>
                <inningId>{2}</inningId>
                </GetPartnership>
                </soap:Body>
                </soap:Envelope>""".format(match_id,series_id,current_inning)

                all_partnerships = []

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction": "http://schema.sportsflash.com.au/Cricket/GetPartnership"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')

                for partner in soup.findAll('partner'):
                    partnership = partner.findAll('batsman')
                    all_partnerships.append({'player_1':partnership[0].find('name').text,'player_1_runs':partnership[0].get('runs'),'player_1_index':partnership[0].get('playerindex'),'player_1_id':\
                            partnership[0].get('playerid'),'player_1_image':self.infoplum_images.find_one({'player_id':partnership[0].get('playerid')})['player_image'],'player_1_balls':\
                            partnership[0].get('ballfaced'),'player_2':partnership[1].find('name').text,'player_2_runs':partnership[1].get('runs'),'player_2_index':partnership[1].get('playerindex'),'player_2_id':\
                            partnership[1].get('playerid'),'player_2_image':self.infoplum_images.find_one({'player_id':partnership[1].get('playerid')})['player_image'],'player_2_balls':partnership[1].get('ballfaced')})

                try:
                    self.current_partnership = all_partnerships[-1]
                except Exception,e:
                    self.current_partnership = {}

                return


        def get_man_of_the_match(self,match_id,series_id):

                body = """<?xml version="1.0" encoding="utf-8"?>
                <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                <soap:Header>
                <AuthenticationHeader xmlns="http://schema.sportsflash.com.au/Cricket/">
                <UserName>TUFETQ==</UserName>
                <Password>TUFEMjg2ODM3MDFAMjAxNg==</Password>
                </AuthenticationHeader>
                </soap:Header>
                <soap:Body>
                <GetManOfTheMatch xmlns="http://schema.sportsflash.com.au/Cricket/">
                <clientId>209</clientId>
                <localeId>en</localeId>
                <seriesId>{0}</seriesId>
                <matchId>{1}</matchId>
                </GetManOfTheMatch>
                </soap:Body>
                </soap:Envelope>""".format(series_id,match_id)

                self.man_of_the_match = {}

                encoded_request = body.encode('utf-8')
                headers = {"Host": "ckt.webservice.sportsflash.com.au", 'Content-Type': "text/xml; charset=UTF-8", "Content-Length": len(encoded_request), "SOAPAction":\
                 "http://schema.sportsflash.com.au/Cricket/GetManOfTheMatch"}
                r = requests.post("http://ckt.webservice.sportsflash.com.au/securewebservice.asmx", data=encoded_request, headers=headers, verify=False)
                soup = BeautifulSoup((r.content),'lxml')

                try:
                    if soup.find('manofthematch').find('bowling').find('over').text:
                        self.man_of_the_match.setdefault('bowling',{}).update({'overs':soup.find('manofthematch').find('bowling').find('over').text,'wickets':\
                            soup.find('manofthematch').find('bowling').find('wicket').text,'runs':soup.find('manofthematch').find('bowling').find('run').text,\
                            'economy':soup.find('manofthematch').find('bowling').find('economy').text})
                    if soup.find('manofthematch').find('batting').find('run').text:
                        self.man_of_the_match.setdefault('batting',{}).update({'runs':soup.find('manofthematch').find('batting').find('run').text,'balls':\
                            soup.find('manofthematch').find('batting').find('ball').text,'six':soup.find('manofthematch').find('batting').find('six').text,\
                            'strike_rate':soup.find('manofthematch').find('batting').find('strikerate').text})

                    self.man_of_the_match.update({'name':soup.find('manofthematch').find('playername').text,'player_id':soup.find('manofthematch').get('playerid'),'player_image':\
                            self.infoplum_images.find_one({'player_id':soup.find('manofthematch').get('playerid')})['player_image']})

                except Exception,e:
                    pass

                return



if __name__=="__main__":

        obj = Infoplum_data_scorecard()
        obj.get_match_list()

