#!/usr/bin/env python
#*--encoding: utf-8 --*

#    visióna
import sys
from elasticsearch import Elasticsearch
from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse

app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("team", type=str, location="args", required=False)
get_args.add_argument("league", type=str, location="args", required=False)
get_args.add_argument("player", type=str, location="args", required=False)
get_args.add_argument("sport_type", type=str, location="args", required=False)

reload(sys)
sys.setdefaultencoding('utf-8')

class GetTeam(restful.Resource):

    def get(self):
        es = Elasticsearch()
        args = get_args.parse_args()
        __body = {"_source":['team_name','team_id','team_flag'],"query": { "and": [ { "match_phrase" :{ "team_autocomplete": {"query": args['team'],"fuzziness":\
                10,"operator":  "and"}}}, {'match': {'sport_type':args['sport_type']}}]}}

        __result = es.search(index='teams',doc_type='teams',body=__body)
        result = [l["_source"] for l in __result["hits"]["hits"]]

        return {'error':False,
                'success':True,
                'data':result}

"""
class GetFootballTeam(restful.Resource):

    def get(self):
        es = Elasticsearch()
        args = get_args.parse_args()
        __body = {"_source":['team_name','team_id'],"query": { "match_phrase" :{ "team_autocomplete": {"query": args['team'],"fuzziness": 10,"operator":  "and"}}}}

        __result = es.search(index='football_teams',doc_type='football_teams',body=__body)
        result = [l["_source"] for l in __result["hits"]["hits"]]

        return {'error':False,
                'success':True,
                'data':result}
"""

class GetLeague(restful.Resource):
        
    def get(self):
        es = Elasticsearch()
        args = get_args.parse_args()
        __body = {"_source":['league_name','league_id'],"query": { "match_phrase" :{ "league_autocomplete": {"query": args['league'],"fuzziness": 10,"operator":  "and"}}}}
        __result = es.search(index='leagues',doc_type='leagues',body=__body)
        result = [l["_source"] for l in __result["hits"]["hits"]]

        return {'error': False,
                'success': True,
                'data': result}

class GetPlayer(restful.Resource):

    def get(self):
        es = Elasticsearch()
        args = get_args.parse_args()
        print args['player']
        __body = {"_source":['name','player_id','player_image'],"query": { "and":[ { "match_phrase_prefix" :{ "name": {"query": args['player'],"fuzziness":\
                10,"operator":  "and"}}}, { "match" : {"sport_type": args['sport_type']}}]}}
        __result = es.search(index='players',doc_type='players',body=__body)
        result = [l["_source"] for l in __result["hits"]["hits"]]

        return {'error': False,
                'success': True,
                'data': result}


api.add_resource(GetTeam, "/fav_team")
#api.add_resource(GetFootballTeam,"/fav_football_team")
api.add_resource(GetLeague, "/fav_league")
api.add_resource(GetPlayer, "/fav_player")
#api.add_resource(GetFootballPlayer, "/fav_football_player")
if __name__=='__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)



