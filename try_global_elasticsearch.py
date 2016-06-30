#!/usr/bin/env python

from elasticsearch import Elasticsearch
import requests
import pymongo
import json
import time
import calendar
from pyfiglet import figlet_format
from termcolor import cprint
import connection

ES_CLIENT = connection.get_elastic_search_connection()

conn = connection.get_mongo_connection()

news_conn = conn.SPORTS_UNITY_NEWS.SPORTS_UNITY_NEWS_ALL
football_player_stats_conn = conn.test.football_player_stats
players_conn = conn.cricket.players
matches_conn = conn.cricket.matches
infoplum_team_flags_conn = conn.test.infoplum_team_flags

class GetTeams:

        def __init__(self,renew_indexes=False):

                self.teams_list = []

                self.settings = {
  "settings": {
    "index": {
      "analysis": {
        "filter": {
          "stemmer": {
            "type": "stemmer",
            "language": "english"
          },
          "autocompleteFilter": {
            "max_shingle_size": "5",
            "min_shingle_size": "2",
            "type": "shingle"
          },
          "stopwords": {
            "type": "stop",
            "stopwords": [
              "_english_"
            ]
          }
        },
        "analyzer": {
          "didYouMean": {
            "filter": [
              "lowercase"
            ],
            "char_filter": [
              "html_strip"
            ],
            "type": "custom",
            "tokenizer": "standard"
          },
          "autocomplete": {
            "filter": [
              "lowercase",
              "autocompleteFilter"
            ],
            "char_filter": [
              "html_strip"
            ],
            "type": "custom",
            "tokenizer": "standard"
          },
          "default": {
            "filter": [
              "lowercase",
              "stopwords",
              "stemmer"
            ],
            "char_filter": [
              "html_strip"
            ],
            "type": "custom",
            "tokenizer": "standard"
          }
        }
      }
    }
  }
}

                self.mappings = {'dynamic': False,
        'properties': {'autocomplete': {'analyzer': 'autocomplete', 'type':'string'},
        'did_you_mean': {'analyzer': 'didYouMean', 'type': 'string'},
        'name': {'copy_to': ['autocomplete','did_you_mean'], 'type': 'string'},
        'home_team': {'copy_to': ['autocomplete', 'did_you_mean'], 'type': 'string'},
        'away_team': {'copy_to': ['autocomplete', 'did_you_mean'], 'type': 'string'},
        'id' : {'index': 'not_analyzed', 'type': 'string'},
        'series_id': {'index': 'not_analyzed', 'type': 'string'},
        'image': {'index': 'not_analyzed', 'type': 'string'},
        'region': {'index': 'not_analyzed', 'type': 'string'},
        'sport_type': {'index': 'not_analyzed', 'type': 'string'},
        'search_type': {'index': 'not_analyzed', 'type': 'string'},
        'home_team_flag': {'index': 'not_analyzed', 'type': 'string'},
        'away_team_flag': {'index': 'not_analyzed', 'type': 'string'},
        'result': {'index': 'not_analyzed', 'type': 'string'},
        'status': {'index': 'not_analyzed', 'type': 'string'},
        'title': {'copy_to': ['autocomplete', 'did_you_mean'], 'type': 'string'},
        'summary': {'index': 'not_analyzed', 'type': 'string'},
        'news': {'copy_to': ['autocomplete', 'did_you_mean'], 'type': 'string'},
        'publish_epoch': {'index': 'not_analyzed', 'type': 'string'},
        'match_widget': {'enabled': False, 'type': 'object'},
        'venue': {'index': 'not_analyzed', 'type': 'string'},
        'home_team_short_name': {'index': 'not_analyzed', 'type': 'string'},
        'away_team_short_name': {'index': 'not_analyzed', 'type': 'string'},
        'news_link': {'index': 'not_analyzed', 'type': 'string'},
        'match_number': {'index': 'not_analyzed', 'type': 'string'},
        }}


                if not ES_CLIENT.indices.exists("all"):
                        self.prep_teams_index()
                        self.index_data()

                if renew_indexes:
                        ES_CLIENT.indices.delete(index="all")
                        self.prep_teams_index()
                        self.index_data()


        def prep_teams_index(self):
                ES_CLIENT.indices.create(index="all", body=self.settings)
                ES_CLIENT.indices.put_mapping(index="all", doc_type="all", body = {"all": self.mappings })
                a = "Mappings updated for  {0}".format("All")
                cprint(figlet_format(a, font='starwars'), attrs=['bold'])
                

        
        def index_data(self):
                
                for article in news_conn.find({}, {'_id': False, 'title': True, 'summary': True, 'news_id': True, 'news': True, 'publish_epoch': True, 'image_link': True, 'type': True, 'favicon': True, 'news_link': True}):
                        if 'type' and 'favicon' in article.keys():
                            article.update({'id': article.pop('news_id'), 'image': article.pop('image_link'), 'sport_type': article.pop('type'), 'title': article.pop('title'),'favicon':\
                                        article.pop('favicon'),'summary': article.pop('summary'), 'news': article.pop('news'), 'publish_epoch': article.pop('publish_epoch'), 'news_link': article.pop('news_link'),'search_type': 'news'})

                            print ES_CLIENT.index(index="all", doc_type="all", body=article)

                for match in matches_conn.find({}, {'_id': False, 'match_name': True, 'match_id': True, 'series_id': True, 'home_team_flag': True, 'away_team_flag': True, 'result': True, 'status': True,\
                                        'home_team': True, 'away_team': True, 'match_time': True, 'match_widget': True, 'venue': True, 'home_team_short_name': True, 'away_team_short_name': True}):

                        if 'home_team_flag' and 'away_team_flag' in match.keys():
                            try:
                                match.update({'name': match['home_team'] + ' vs ' + match['away_team'], 'id': match.pop('match_id'), 'series_id': match.pop('series_id'), 'home_team_flag': match.pop('home_team_flag'),\
                                        'away_team_flag': match.pop('away_team_flag'), 'result': match.pop('result'), 'status': match.pop('status'), 'sport_type': 'cricket', 'search_type': \
                                        'match', 'home_team': match.pop('home_team'), 'away_team': match.pop('away_team'), 'publish_epoch': match.pop('match_time'), 'venue': match.pop('venue'),\
                                        'home_team_short_name': match.pop('home_team_short_name'), 'away_team_short_name': match.pop('away_team_short_name'), 'match_widget': match.pop('match_widget'),\
                                        'match_number': match.pop('match_name')})

                                print ES_CLIENT.index(index="all", doc_type="all", body=match)
                            except Exception,e:
                                print e

                
                teams = []
                leagues_list = []

                list_of_league_ids = ['1269','1399','1229','1221','1204','364']
                for league_id in list_of_league_ids:
                        response = requests.get('http://ScoresLB-822670678.ap-northeast-2.elb.amazonaws.com/get_league_standings?league_id=%s'%league_id)
                        data = json.loads(response.content)
                        for team in data['data']:
                                team.update({'name':team.pop('team_name'),'id':team.pop('team_id'),'sport_type':team.pop('sport_type'),'image':team.pop('flag_image'), 'search_type': 'team', 'publish_epoch':calendar.timegm(time.gmtime())})
                                print teams,'*'*10
                #for name in teams:
                                print ES_CLIENT.index(index="all", doc_type="all", body=team)


                team_ids_list = []
                
                for player in players_conn.find(projection={'_id':False,'team':True,'team_id':True,'sport_type':True}):
                    if player['team_id'] not in team_ids_list:
                        try:
                            team_flag = infoplum_team_flags_conn.find_one({'team_id':player['team_id']})['team_flag']
                        except Exception,e:
                            team_flag = ''
                        print player['team_id'],'*'*10
                        self.teams_list.append({'name': player['team'], 'id': player['team_id'], 'image': team_flag, 'sport_type': player['sport_type'], 'search_type': 'team', 'publish_epoch': calendar.timegm(time.gmtime())})
                        team_ids_list.append(player['team_id'])
                    else:
                        pass

                for team in self.teams_list:
                        if team['image']:
                            print team['image']
                            print ES_CLIENT.index(index="all", doc_type="all", body=team)
                        else:
                            print 'no flag'

                response = requests.get('http://ScoresLB-822670678.ap-northeast-2.elb.amazonaws.com/get_football_leagues')
                data = json.loads(response.content)

                for league in data['data']:
                    try:
                        league.update({'name': league.pop('league_name'), 'id': league.pop('league_id'), 'image': league.pop('flag_image',''), 'sport_type': 'football', 'region': league.pop('region'), 'search_type': 'league',\
                                'publish_epoch': calendar.timegm(time.gmtime())})
                        print ES_CLIENT.index(index="all", doc_type="all", body=league)
                    except Exception,e :
                        print '@@@@@@@@@@',e


                for name in players_conn.find({}, {'_id':False,'name':True,'player_id':True,'team_id':True,'player_image':True,'sport_type':True}):
                    name.update({'name': name.pop('name'), 'id': name.pop('player_id'), 'image': name.pop('player_image'), 'sport_type': name.pop('sport_type'), 'search_type': 'player'})
                    print ES_CLIENT.index(index='all',doc_type='all',body=name)
                
                for player in football_player_stats_conn.find({}, {'_id':False,'name':True,'player_id':True,'team_id':True,'player_image':True,'sport_type':True}):
                    if 'player_id' in player.keys():
                        player.update({'name': player.pop('name'), 'id': player.pop('player_id'), 'image': player.pop('player_image'), 'sport_type': player.pop('sport_type'), 'search_type': 'player'})
                        print ES_CLIENT.index(index='all',doc_type='all',body=player)

                

if __name__=="__main__":

        obj = GetTeams(renew_indexes=True)
        

