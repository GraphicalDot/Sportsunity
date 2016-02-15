#!/usr/bin/env python

from elasticsearch import Elasticsearch
from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
#from teams_elasticsearch import GetTeams
import pymongo
from operator import itemgetter

app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("season_key", type=str, location="args", required=False)

class GetRecentSeasons(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.season_fixtures = db.season_fixtures

        def get(self):
                
                recent_seasons = list(self.season_fixtures.find(projection={'_id':False,'season_name':True,'start_date':True,'season_key':True}))
                
                return {'success':True,
                        'error':False,
                        'data':sorted(recent_seasons),
                        }

class GetSeasonFixtures(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.season_fixtures = db.season_fixtures

        def get(self):

                args = get_args.parse_args()

                season_fixtures = list(self.season_fixtures.find({'season_key':args['season_key']},projection={'_id':False,'season_name':True,'season_key':True,'fixtures':True}))

                return {'success':True,
                        'error':False,
                        'data':sorted(season_fixtures)
                        }

class GetSeasonTable(restful.Resource):

        def __init__(self):
                
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.season_fixtures = db.season_fixtures

        def get(self):
                
                args = get_args.parse_args()

                points_table = list(self.season_fixtures.find({'season_key':args['season_key']},projection={'_id':False,'season_name':True,'season_key':True,'points_table':True}))
        
                return {'success':True,
                        'error':False,
                        'data':sorted(points_table)
                        }

class GetSeasonStats(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.season_fixtures = db.season_fixtures

        def get(self):

                args = get_args.parse_args()

                season_stats = list(self.season_fixtures.find({'season_key':args['season_key']},projection={'_id':False,'season_name':True,'season_key':True,'stats':True}))

                return {'success':True,
                        'error':False,
                        'data':season_stats,
                        }

class GetSeasonTopBatsmen(restful.Resource):

            def __init__(self):

                    conn = pymongo.MongoClient()
                    db = conn.admin
                    db.authenticate('shivam','mama123')
                    db = conn.test
                    self.season_fixtures = db.season_fixtures

            def get(self):
                    
                    args = get_args.parse_args()

                    season_top_batsmen = list(self.season_fixtures.find({'season_key':args['season_key']},projection={'_id':False,'season_name':True,'season_key':True,'top_batsmen':True}))

                    return {'success':True,
                            'error':False,
                            'data':season_top_batsmen,
                            }

class GetSeasonTopBowlers(restful.Resource):

            def __init__(self):

                    conn = pymongo.MongoClient()
                    db = conn.admin
                    db.authenticate('shivam','mama123')
                    db = conn.test
                    self.season_fixtures = db.season_fixtures

            def get(self):
                    
                    args = get_args.parse_args()

                    season_top_bowlers = list(self.season_fixtures.find({'season_key':args['season_key']},projection={'_id':False,'season_name':True,'season_key':True,'top_bowlers':True}))

                    return {'success':True,
                            'error':False,
                            'data':season_top_bowlers,
                            }


api.add_resource(GetRecentSeasons,'/get_recent_seasons')
api.add_resource(GetSeasonFixtures, '/get_season_fixtures')
api.add_resource(GetSeasonTable, '/get_season_table')
api.add_resource(GetSeasonStats,'/get_season_stats')
api.add_resource(GetSeasonTopBatsmen,'/get_season_top_batsmen')
api.add_resource(GetSeasonTopBowlers,'/get_season_top_bowlers')


if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5800 , debug = True)



                


                
                
        

        


