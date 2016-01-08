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
                db = conn.stats
                self.cricket_teams = db.cricket_teams

                self.settings={'settings': {'analysis': {'analyzer': {'custom_analyzer': {'filter': ['lowercase',
        'asciifolding'],
        'tokenizer': 'ngram_tokenizer', 'type':'custom'},
        'keyword_analyzer': {'filter': ['lowercase', 'asciifolding'],
        'tokenizer': 'keyword',
        'type': 'custom'},
        'shingle_analyzer': { 'filter': ['lowercase', 'asciifolding','shingle_tokenizer'],
        'tokenizer': 'ngram_tokenizer',
        'type': 'custom'}},
        'filter': {'shingle_tokenizer': {'max_shingle_size': '5',
        'min_shingle_size': '2',
        'type': 'shingle'}},
        'tokenizer': {'ngram_tokenizer': {'max_gram': '100',
        'min_gram': '2',
        'token_chars': ['letter', 'digit'],
        'type': 'edgeNGram'}}}

        }}

                self.mappings = {'dynamic': 'strict',
        'properties': {'team_autocomplete': {'analyzer': 'custom_analyzer', 'type':'string'},
        'team_name': {'copy_to': ['team_autocomplete'], 'type': 'string'},
        'team_points': {'index': 'not_analyzed', 'type': 'string'},
        'league_id': {'index': 'not_analyzed', 'type': 'string'},
        'team_id' : {'index': 'not_analyzed', 'type': 'string'},
        'stand_season': {'index': 'not_analyzed', 'type': 'string'},
        'flag_image': {'index': 'not_analyzed', 'type': 'string'},
        'games_won': {'index': 'not_analyzed', 'type': 'string'},
        'games_lost' : {'index': 'not_analyzed', 'type': 'string'},
        'season': {'index': 'not_analyzed', 'type': 'long'},
        'position': {'index': 'not_analyzed', 'type': 'long'},
        'games_played': {'index': 'not_analyzed', 'type': 'string'},
        'games_drawn' : {'index': 'not_analyzed', 'type': 'string'},
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
                cprint(figlet_format(a, font='mini'), attrs=['bold'])
                

        
        def index_data(self):
                response = requests.get('http://52.74.142.219:8000/get_league_standings?league_id=1269')
                data = json.loads(response.content)
                for team in data['data']:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team)

                response = requests.get('http://52.74.142.219:8000/get_league_standings?league_id=1399')
                data = json.loads(response.content)
                for team in data['data']:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team)
                
                response = requests.get('http://52.74.142.219:8000/get_league_standings?league_id=1229')  
                data = json.loads(response.content)
                for team in data['data']:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team)

                response = requests.get('http://52.74.142.219:8000/get_league_standings?league_id=1221')
                data = json.loads(response.content)
                for team in data['data']:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team)

                response = requests.get('http://52.74.142.219:8000/get_league_standings?league_id=1204')
                data = json.loads(response.content)
                for team in data['data']:
                        print ES_CLIENT.index(index="teams", doc_type="teams", body=team)
                for team in cricket_teams.find(projection={'_id':False,'type':False}):
                    print ES_CLIENT.index(index="teams", doc_type="teams", body=team)



if __name__=="__main__":

        obj = GetTeams(renew_indexes=True)
        
        

       
