#!/usr/bin/env python

from elasticsearch import Elasticsearch
import requests
import pymongo
import json
from pyfiglet import figlet_format
from termcolor import cprint

ES_CLIENT = Elasticsearch()

class GetTeams:

        def __init__(self,renew_indexes=False):

                conn = pymongo.MongoClient()
                db = conn.cricket
                db1 = conn.test
                self.players = db.players
                self.infoplum_team_flags = db1.infoplum_team_flags
                self.teams_list = []           


                self.settings={'settings': {'analysis': {'analyzer': {'custom_analyzer': {'filter': ['lowercase',
        'asciifolding','edge_ngram'],
        'tokenizer': 'ngram_tokenizer', 'type':'custom'}},
        'filter': {'edge_ngram': {'max_gram': '100',
        'min_gram': '2',
        'type': 'edge_ngram'}},
        'tokenizer': {'ngram_tokenizer': {'max_gram': '100',
        'min_gram': '2',
        'token_chars': ['letter', 'digit'],
        'type': 'edgeNGram'}}}

        }}

                self.mappings = {'dynamic': 'strict',
        'properties': {'team_autocomplete': {'analyzer': 'custom_analyzer', 'type':'string'},
        'team_name': {'copy_to': ['team_autocomplete'], 'type': 'string'},
        #'team_points': {'index': 'not_analyzed', 'type': 'string'},
        #'league_id': {'index': 'not_analyzed', 'type': 'string'},
        'team_id' : {'index': 'not_analyzed', 'type': 'string'},
        # 'stand_season': {'index': 'not_analyzed', 'type': 'string'},
        # 'stand_group' : {'index': 'not_analyzed', 'type': 'string'},
        'team_flag': {'index': 'not_analyzed', 'type': 'string'},
        # 'league_name': {'index': 'not_analyzed', 'type': 'string'},
        # 'games_won': {'index': 'not_analyzed', 'type': 'string'},
        # 'games_lost' : {'index': 'not_analyzed', 'type': 'string'},
        # 'season': {'index': 'not_analyzed', 'type': 'long'},
        # 'position': {'index': 'not_analyzed', 'type': 'long'},
        # 'games_played': {'index': 'not_analyzed', 'type': 'string'},
        # 'games_drawn' : {'index': 'not_analyzed', 'type': 'string'},
        'sport_type': {'index': 'not_analyzed', 'type': 'string'}
        }}


                if not ES_CLIENT.indices.exists("teams"):
                        self.prep_teams_index()
                        self.index_data()

                if renew_indexes:
                        ES_CLIENT.indices.delete(index="teams")
                        self.prep_teams_index()
                        self.index_data()


        def prep_teams_index(self):
                ES_CLIENT.indices.create(index="teams", body=self.settings)
                ES_CLIENT.indices.put_mapping(index="teams", doc_type="teams", body = {"teams": self.mappings })
                a = "Mappings updated for  {0}".format("teams")
                cprint(figlet_format(a, font='starwars'), attrs=['bold'])
                

        
        def index_data(self):
                teams = []
                list_of_league_ids = ['1269','1399','1229','1221','1204']
                for league_id in list_of_league_ids:
                        response = requests.get('http://52.74.75.79:8000/get_league_standings?league_id=%s'%league_id)
                        data = json.loads(response.content)
                        for team in data['data']:
                                teams.append({'team_name':team.pop('team_name'),'team_id':team.pop('team_id'),'sport_type':team.pop('sport_type'),'team_flag':team.pop('flag_image')})
                print teams,'*'*10
                for team_name in teams:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team_name)

                #for team in self.cricket_teams.find(projection={'_id':False}):
                 #       print ES_CLIENT.index(index="teams", doc_type="teams", body=team)

                team_ids_list = []
                
                for player in self.players.find(projection={'_id':False,'team':True,'team_id':True,'sport_type':True}):
                    if player['team_id'] not in team_ids_list:
                        try:
                            team_flag = self.infoplum_team_flags.find_one({'team_id':player['team_id']})['team_flag']
                        except Exception,e:
                            team_flag = ''
                        print player['team_id'],'*'*10
                        self.teams_list.append({'team_name':player['team'],'team_id':player['team_id'],'team_flag':team_flag,'sport_type':player['sport_type']})
                        team_ids_list.append(player['team_id'])
                    else:
                        pass

                for team in self.teams_list:
                        if team['team_flag']:
                            print team['team_flag']
                            print ES_CLIENT.index(index="teams", doc_type="teams", body=team)
                        else:
                            print 'no flag'

                

if __name__=="__main__":

        obj = GetTeams(renew_indexes=True)
        
        

       
