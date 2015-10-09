#!/usr/bin/env python

import sys
import os
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, app, jsonify
from flask.ext import restful
import json
import time
from flask.ext.restful import Api, Resource, reqparse
from live_cric_scores import CricketScores, CricketFixtures 

app = Flask(__name__)
api = restful.Api(app)


get_args = reqparse.RequestParser()
get_args.add_argument("date", type=str, location="args", required=False)

get_fixtures_args = reqparse.RequestParser()
get_fixtures_args.add_argument("date", type=str, location="args", required=False)

class LiveCricketScore(restful.Resource):
        
        #def __init__(self):
         #       obj = CricketScores()


        def get(self):
                pattern = "%d-%b-%Y"
                args = get_args.parse_args()
                if args['date']:
                        match_date = int(time.mktime(time.strptime(args['date'],pattern)))
                        obj = CricketScores('http://synd.cricbuzz.com/j2me/1.0/livematches.xml')
                        result = obj.send_scores(match_date)
                        print result
                        return {"error":False,
                                "success":True,
                                "result":result}
                else:
                        match_date = int(time.mktime(time.strptime(time.strftime("%d-%b-%Y"),pattern)))
                        obj = CricketScores('http://synd.cricbuzz.com/j2me/1.0/livematches.xml')
                        result = obj.send_scores(match_date)
                        return {"error":False,
                                "success":True,
                                "result":result}



class UpcomingFixtures(restful.Resource):

        def get(self):
                pattern = "%d-%b-%Y"
                args = get_fixtures_args.parse_args()
                try:

                    if args['date']:
                            fixture_date = int(time.mktime(time.strptime(args['date'],pattern)))
                            obj = CricketFixtures('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')
                            result = obj.send_fixtures(fixture_date)
                            print result
                            return {"error":False,
                                    "success":True,
                                    "result":result}
                    else:
                            obj = CricketFixtures('http://synd.cricbuzz.com/j2me/1.0/sch_calender.xml')
                            result = obj.send_fixtures_if_no_date()
                            return {"error":False,
                                    "success":True,
                                    "result":result}
                except Exception,e:
                    return """Troubleshooting steps: Firstly, please check the URL you are entering. Secondly, please check the date pattern you are entering the right pattern is '18-Sep-2015'"""



'''
class Cricket_Scorecard(restful.Resource):
                                            #todo
        def get()
'''



api.add_resource(LiveCricketScore, "/live_score")
api.add_resource(UpcomingFixtures, "/upcoming_fixtures")

if __name__=="__main__":
        app.run(host = "0.0.0.0", port = 5000, debug = True)
                
