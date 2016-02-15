#!/usr/bin/env python
import requests
import json
import pprint
from operator import itemgetter
from datetime import datetime
import pymongo

class CricketSeason:

        def __init__(self,url):
                header = {'access_key':'6be398607be5a5e44ff0f0d2244146e6', 'secret_key':'1213aa15ed5bc5f9abd3fde62df4a3c1', 'app_id':'123', 'device_id':'123'}
                res = requests.post(url,header)
                data = json.loads(res.content)
                self.auth_code = data['auth']['access_token']
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.season_fixtures = db.season_fixtures


        def get_recent_seasons(self):
                url = 'https://api.litzscore.com/rest/v2/recent_seasons/?access_token=%s'%self.auth_code
                res = requests.get(url)
                data = json.loads(res.content)
                for recent_season in data['data']:
                    self.get_season_fixtures(recent_season['key'])
                    self.get_season_stats(recent_season['key'])
                    self.get_season_top_player_stats(recent_season['key'])

                    if self.participating_teams and len(self.participating_teams)>2:
                            self.get_points_table(recent_season['key'])
                            try:
                                self.season_fixtures.update({'season_key':recent_season['key']},{'$set':{'season_key':recent_season['key'],'season_name':recent_season['name'],'fixtures':\
                                        self.new_list,'start_date':recent_season['start_date']['iso'],'participating_teams':self.participating_teams,'points_table':self.table,'stats':self.season_stats,'top_batsmen':\
                                        self.season_batting_stats,'top_bowlers':self.season_bowling_stats}},upsert=True)

                            except Exception,e:
                                self.season_fixtures.update({'season_key':recent_season['key']},{'$set':{'season_key':recent_season['key'],'season_name':recent_season['name'],'fixtures':\
                                        '','start_date':recent_season['start_date']['iso'],'participating_teams':self.participating_teams,'points_table':'','stats':self.season_stats,'top_batsmen':'','top_bowlers':''}},upsert=True)

                    elif self.participating_teams and not len(self.participating_teams)>2:
                            try:
                                self.season_fixtures.update({'season_key':recent_season['key']},{'$set':{'season_key':recent_season['key'],'season_name':recent_season['name'],'fixtures':\
                                        self.new_list,'start_date':recent_season['start_date']['iso'],'participating_teams':self.participating_teams,'points_table':'','stats':self.season_stats,'top_batsmen':\
                                        self.season_batting_stats,'top_bowlers':self.season_bowling_stats}},upsert=True)

                            except Exception,e:
                                    self.season_fixtures.update({'season_key':recent_season['key']},{'$set':{'season_key':recent_season['key'],'season_name':recent_season['name'],'fixtures':\
                                            '','start_date':recent_season['start_date']['iso'],'participating_teams':self.participating_teams,'points_table':'','stats':'','top_batsmen':'','top_bowlers':''}},upsert=True)
                    else:
                            pass



                #for season in self.season_fixtures.find():
                #        if len(season['participating_teams'])>2:
                #                self.get_points_table(season['season_key'])

                 #       else:
                  #              pass
                   #             #self.season_fixtures.update({'season_key':season['season_key']},{'$set':{'points_table':''}})
                    #    self.season_fixtures.update({'season_key':season['season_key']},{'$set':{'points_table':self.table}})



        def get_season_fixtures(self,key):
                fixtures = []
                self.participating_teams = []
                url = 'https://api.litzscore.com/rest/v2/season/{0}/?access_token={1}'.format(key,self.auth_code)
                res = requests.get(url)
                data = json.loads(res.content)
                date = datetime.isoformat(datetime.utcnow())
                try:
                        for match_key in data['data']['season']['matches'].keys():
                            if not data['data']['season']['matches'][match_key]['start_date']['iso']<date:
                                    fixtures.append({'match_name':data['data']['season']['matches'][match_key]['title'],'match_key':match_key,'date':data['data']['season']['matches'][match_key]['start_date']['iso'],\
                                            'info':''})
                            else:
                                    fixtures.append({'match_name':data['data']['season']['matches'][match_key]['title'],'match_key':match_key,'date':data['data']['season']['matches'][match_key]['start_date']['iso'],\
                                            'info':data['data']['season']['matches'][match_key]['msgs']['info']})

                        self.new_list = sorted(fixtures,key=itemgetter('date'))


                        """
                        if not new_list[-1]['info']<date:
                                self.new_list = new_list
                        else:
                                new_list = []
                                for match in fixtures:
                                        new_list.append({'match_name':match['match_name'],'match_key':match['match_key'],'info':data['data']['season']['matches'][match['match_key']]['msgs']['info']})
                                self.new_list = new_list
                        """

                except Exception,e:
                        pass

                try:
                        for team_key in data['data']['season']['teams'].keys():
                                self.participating_teams.append({'team_name':data['data']['season']['teams'][team_key]['name'].strip()})

                except Exception,e:
                        pass

                return

       
        def get_points_table(self,key):
                self.table = {}
                url = 'https://api.litzscore.com/rest/v2/season/{0}/points/?access_token={1}'.format(key,self.auth_code)
                res = requests.get(url)
                data = json.loads(res.content)
                try:
                        for group in data['data']['points']['rounds'][0]['groups']:
                                self.table.setdefault(group['name'],[]).append(group['teams'])
                except Exception,e:
                        for group in data['data']['points']['rounds'][0]['groups']:
                                self.table.setdefault(group['name'],[]).append(group['teams'])

                        #self.table = [{data['data']['points']['rounds'][0]['groups'][0]['name']:data['data']['points']['rounds'][0]['groups'][0]['teams']}]

                return

        def get_season_stats(self,key):
                self.season_stats = []
                url = 'https://api.litzscore.com/rest/v2/season/{0}/stats/?access_token={1}'.format(key,self.auth_code)
                res = requests.get(url)
                data = json.loads(res.content)
                try:
                        self.season_stats.append({'total_sixes':data['data']['stats']['sixes'],'total_runs':data['data']['stats']['runs'],'total_fours':data['data']['stats']['fours']})
                except Exception,e:
                        print e
                        pass

                return

        def get_season_top_player_stats(self,key):
                self.season_batting_stats = []
                self.season_bowling_stats = [] 
                url = 'https://api.litzscore.com/rest/v2/season/{0}/stats/?access_token={1}'.format(key,self.auth_code)
                res = requests.get(url)
                data = json.loads(res.content)

                try:
                    for top_batsman in data['data']['stats']['batting']['most_runs']:
                            try:
                                    self.season_batting_stats.append({'player':top_batsman['full_name'],'runs':top_batsman['stats']['batting']['runs']})
                            except Exception,e:
                                    print e
                                    pass
                except Exception,e:
                    pass

                try:
                    for top_bowler in data['data']['stats']['bowling']['most_wickets']:
                            try:
                                    self.season_bowling_stats.append({'player':top_bowler['full_name'],'wickets':top_bowler['stats']['bowling']['wickets']})
                            except Exception,e:
                                    print e
                                    pass
                except Exception,e:
                    pass

                return 


if __name__=='__main__':
        obj = CricketSeason('https://api.litzscore.com/rest/v2/auth/')
        obj.get_recent_seasons()
