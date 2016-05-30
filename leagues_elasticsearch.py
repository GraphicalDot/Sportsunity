#!/usr/bin/env python

import requests
import json
from pyfiglet import figlet_format
from termcolor import cprint
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection


ES_CLIENT = connection.get_elastic_search_connection()


class GetTeams:

        def __init__(self,renew_indexes=False):

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
                                 'properties': {'league_autocomplete': {'analyzer': 'custom_analyzer', 'type':'string'},
                                                'league_name': {'copy_to': ['league_autocomplete'], 'type': 'string'},
                                                'league_id': {'index': 'not_analyzed', 'type': 'string'},
                                                'season': {'index': 'not_analyzed', 'type': 'long'},
                                                'flag_image':{'index': 'not_analyzed', 'type': 'string'},
                                                'region' : {'index': 'not_analyzed', 'type': 'string'},
                                                }}


                if not ES_CLIENT.indices.exists("leagues"):
                        self.prep_teams_index()
                        self.index_data()

                if renew_indexes:
                        ES_CLIENT.indices.delete(index="leagues")
                        self.prep_teams_index()
                        self.index_data()


        def prep_teams_index(self):
                ES_CLIENT.indices.create(index="leagues", body=self.settings)
                ES_CLIENT.indices.put_mapping(index="leagues", doc_type="leagues", body = {"leagues": self.mappings })
                a = "Mappings updated for  {0}".format("leagues")
                cprint(figlet_format(a, font='starwars'), attrs=['bold'])



        def index_data(self):
                response = requests.get('http://ScoresLB-822670678.ap-northeast-2.elb.amazonaws.com/get_football_leagues')
                data = json.loads(response.content)
                for league in data['data']:
                        print ES_CLIENT.index(index="leagues", doc_type="leagues", body=league)


if __name__=="__main__":
        obj = GetTeams(renew_indexes=True)

       
