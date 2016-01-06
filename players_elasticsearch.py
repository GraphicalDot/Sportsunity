#!/usr/bin/env python

from elasticsearch import Elasticsearch
import requests
import json
import pymongo
from pyfiglet import figlet_format
from termcolor import cprint

ES_CLIENT = Elasticsearch()

class GetPlayers:

        def __init__(self,renew_indexes=False):

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
        'properties': {'player_autocomplete': {'analyzer': 'custom_analyzer', 'type':'string'},
        'name': {'copy_to': ['player_autocomplete'], 'type': 'string'},
        'league_id': {'index': 'not_analyzed', 'type': 'string'},
        'nationality': {'index': 'not_analyzed', 'type': 'string'},
        'position' : {'index': 'not_analyzed', 'type': 'string'},
        'team_id' : {'index': 'not_analyzed', 'type': 'string'},
        'goals' : {'index': 'not_analyzed', 'type': 'string'},
        'jersey' : {'index': 'not_analyzed', 'type': 'string'},
        'yellow_cards' : {'index': 'not_analyzed', 'type': 'string'},
        'red_cards' : {'index': 'not_analyzed', 'type': 'string'},
        'age' : {'index': 'not_analyzed', 'type': 'string'}
        }}


                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.mydb
                self.mycollection = db.mycollection
                
                db1 = conn.stats
                self.cricket_players = db1.cricket_players

                if not ES_CLIENT.indices.exists("players"):
                        self.prep_teams_index()
                        self.index_data()

                if renew_indexes:
                        ES_CLIENT.indices.delete(index="players")
                        self.prep_teams_index()
                        self.index_data()


        def prep_teams_index(self):
                ES_CLIENT.indices.create(index="players", body=self.settings)
                ES_CLIENT.indices.put_mapping(index="players", doc_type="players", body = {"players": self.mappings })
                a = "Mappings updated for  {0}".format("players")
                cprint(figlet_format(a, font='starwars'), attrs=['bold'])
                

        
        def index_data(self):
                for player in self.mycollection.find(projection={'_id':False}):
                        print ES_CLIENT.index(index='players',doc_type='players',body=player)
                for player in self.cricket_players.find(projection={'_id':False}):
                        print ES_CLIENT.index(index='players',doc_type='players',body=player)


if __name__=="__main__":

        obj = GetPlayers(renew_indexes=True)
        
        

       
