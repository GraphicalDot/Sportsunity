#!/usr/bin/env python

from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
import pymongo
from operator import itemgetter

app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()

get_args.add_argument("season_key", type=str, location="args", required=False)
get_args.add_argument("team_id", type=str, location="args", required=False)
get_args.add_argument("player_id", type=str, location="args", required=False)
get_args.add_argument('match_id', type=str, location="args", required=False)

class GetRecentSeasons(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum = db.test_infoplum

        def get(self):
                
                recent_seasons = list(self.test_infoplum.find(projection={'_id':False,'series_name':True,'start_date':True,'end_date':True,'series_id':True,'result':True}))

                recent_series = sorted(recent_seasons,key=itemgetter('start_date'),reverse=True)
                
                return {'success':True,
                        'error':False,
                        'data':recent_series,
                        }

class GetSeasonFixtures(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum = db.test_infoplum

        def get(self):

                args = get_args.parse_args()

                season_fixtures = list(self.test_infoplum.find({'series_id':args['season_key']},projection={'_id':False,'series_name':True,'series_id':True,'fixtures':True}))

                return {'success':True,
                        'error':False,
                        'data':sorted(season_fixtures)
                        }

class GetMatchScorecard(restful.Resource):
        
        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_matches = db.test_infoplum_matches

        def get(self):
                
                args = get_args.parse_args()

                match_scorecard = list(self.test_infoplum_matches.find({'series_id':args['season_key'],'match_id':args['match_id']},projection={'_id':False,'series_name':True,'series_id':True,'match_name':\
                        True,'match_id':True,'status':True,'result':True,'home_team':True,'match_time':True,'away_team':True,'scorecard':True}))

                return {'success':True,
                        'error':False,
                        'data' : match_scorecard,
                        }


class GetMatchCommentary(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_commentary = db.test_infoplum_commentary

        def get(self):
                
                args = get_args.parse_args()

                commentary = list(self.test_infoplum_commentary.find({'series_id':args['season_key'],'match_id':args['match_id']},projection={'_id':False,'series_name':True,'series_id':True,'match_name':\
                        True,'match_id':True,'commentary':True}))


                if commentary:
                    match_commentary = sorted(commentary[0]['commentary'],key=itemgetter('commentary_id'),reverse=True)
                else:
                    match_commentary = []


                try:
                    return {'success':True,
                            'error':False,
                            'data' : match_commentary,
                            }

                except Exception,e:
                    return {'success':False,
                            'error':True,
                            }



class GetSeasonTable(restful.Resource):

        def __init__(self):
                
                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum = db.test_infoplum

        def get(self):
                
                args = get_args.parse_args()

                points_table = list(self.test_infoplum.find({'series_id':args['season_key']},projection={'_id':False,'series_name':True,'series_id':True,'season_table':True}))
        
                return {'success':True,
                        'error':False,
                        'data':sorted(points_table)
                        }

class GetTeamSquad(restful.Resource):
        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_players = db.test_infoplum_players

        def get(self):

                args = get_args.parse_args()

                squad = list(self.test_infoplum_players.find({'team_id':args['team_id']},projection={'_id':False,'team_id':True,'team':True,'player_id':True,'name':True}))

                return {'success':True,
                        'error':False,
                        'data':squad
                        }


class GetPlayerStats(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_players = db.test_infoplum_players

        def get(self):

                args = get_args.parse_args()

                player_stats = list(self.test_infoplum_players.find({'player_id':args['player_id']},projection={'_id':False,'info':True,'player_image':True,'player_id':True,'statistics':True}))

                return {'success':True,
                        'error':False,
                        'data':player_stats
                        }

"""
class GetMatchList(restful.Resource):

        def __init__(self):

                conn = pymongo.MongoClient()
                db = conn.admin
                db.authenticate('shivam','mama123')
                db = conn.test
                self.test_infoplum_matches = db.test_infoplum_matches

        def get(self):

                args = get_args.parse_args()

"""

"""
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
"""

class GetMatchSummary(restful.Resource):

            def __init__(self):

                    conn = pymongo.MongoClient()
                    db = conn.admin
                    db.authenticate('shivam','mama123')
                    db = conn.test
                    self.test_infoplum_matches = db.test_infoplum_matches

            def get(self):
                    
                    args = get_args.parse_args()

                    summary = list(self.test_infoplum_matches.find({'series_id':args['season_key'],'match_id':args['match_id']},projection={'_id':False,'series_name':True,'series_id':True,'match_id':\
                            True,'status':True,'result':True,'start_date':True,'match_time':True,'home_team':True,'away_team':True,'venue':True,'summary':True}))

                    return {'success':True,
                            'error':False,
                            'data':summary,
                            }

                    
"""
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
"""

api.add_resource(GetRecentSeasons,'/get_recent_series')
api.add_resource(GetSeasonFixtures, '/get_series_fixtures')
api.add_resource(GetSeasonTable, '/get_season_table')
api.add_resource(GetTeamSquad,'/get_team_squad')
api.add_resource(GetPlayerStats,'/get_player_stats')
api.add_resource(GetMatchSummary,'/get_match_summary')
api.add_resource(GetMatchScorecard,'/get_match_scorecard')
api.add_resource(GetMatchCommentary,'/get_match_commentary')

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5300 , debug = True)



                


                
                
        

        


