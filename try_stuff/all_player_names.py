#!/usr/bin/env python

from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
import pymongo


app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("team_id", type=str, location="args", required=False)
get_args.add_argument("sport_type", type=str, location="args", required=False)

class GetPlayerNames(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.football_player_stats = db.football_player_stats
		self.player_stats = db.player_stats

        def get(self):

                args = get_args.parse_args()
		
                cricket_players = list(self.player_stats.find(projection={'_id':False,'team_name':True,'name':True,'player_id':True,'sport_type':True}))

                football_players = list(self.football_player_stats.find(projection={'_id':False,'team_name':True,'name':True,'player_id':True,'sport_type':True}))

		result = cricket_players+football_players

                return {'success':True,
                        'error':False,
                        'data':result,
                        }

class GetAllCricketTeams(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_players = db.test_infoplum_players
                self.teams_list = []

        def get(self):
                
                for player in self.test_infoplum_players.find():
                    if player['team'] not in self.teams_list:
                        self.teams_list.append(player['team'])
                    else:
                        pass 

                return {'success':True,
                        'error':False,
                        'data':self.teams_list,
                        }            


api.add_resource(GetPlayerNames, '/get_player_names')
api.add_resource(GetAllCricketTeams, '/get_cricket_teams')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 6900 , debug = True)



                


                
                
        

        


