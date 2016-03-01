#!/usr/bin/env python

from elasticsearch import Elasticsearch
from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
#from teams_elasticsearch import GetTeams
import pymongo


app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("team_id", type=str, location="args", required=False)
get_args.add_argument("player", type=str, location="args", required=False)
get_args.add_argument("sport_type", type=str, location="args", required=False)
get_args.add_argument("player_id", type=str, location="args", required=False)

class GetSquad(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.football_player_stats = db.football_player_stats

        def get(self):
                
                args = get_args.parse_args()

                """
                try:
                    #team_name = args['team'].lower().split(' ')[0]+'-'+args['team'].lower().split(' ')[1]+'-'+args['team'].lower().split(' ')[2]
                except Exception,e:
                    try:
                        team_name = args['team'].lower().split(' ')[0]+'-'+args['team'].lower().split(' ')[1]
                    except Exception,e:
                        team_name = args['team'].lower()

                print team_name
                """

                squad = list(self.football_player_stats.find({'team_id':args['team_id']},projection={'_id':False,'team':True,'team_id':True,'team':True,'short_name':True,'image':True,'Goals':\
                        True,'Assists':True,'Games':True,'Nationality':True,'Position':True,'Jersey':True,'Age':True,'Red':True,'Yellow':True,'player_id':True}))
                
                return {'success':True,
                        'error':False,
                        'data':sorted(squad),
                        }

class GetPlayerProfile(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.football_player_stats = db.football_player_stats

        def get(self):

                args = get_args.parse_args()

                profile = list(self.football_player_stats.find({'player_id':args['player_id']},projection={'_id':False,'team':True,'name':True,'player_id':True,'player_image':True,'profile':True,'other_competitions':True}))

                return {'success':True,
                        'error':False,
                        'data':profile,
                        }

        


api.add_resource(GetSquad,'/get_football_team_squad')
api.add_resource(GetPlayerProfile, '/get_football_player_profile')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5600 , debug = True)



                


                
                
        

        


