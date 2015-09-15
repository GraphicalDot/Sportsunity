#!/usr/bin/env python

import sys
import os
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask import Flask, app, jsonify
from flask.ext import restful
import json
import time
from flask.ext.restful import Api, Resource, reqparse
from live_cric_scores import CricketScores

app = Flask(__name__)
api = restful.Api(app)


get_args = reqparse.RequestParser()
get_args.add_argument("date", type=str, location="args", required=False)

class LiveCricketScore(restful.Resource):
        
        #def __init__(self):
         #       obj = CricketScores()


        def get(self):
                pattern = "%d-%b-%Y"
                args = get_args.parse_args() 
                match_date = int(time.mktime(time.strptime(args['date'],pattern)))
                obj = CricketScores('http://synd.cricbuzz.com/j2me/1.0/livematches.xml')
                result = obj.send_scores(match_date)
                print result
                return {"error":False,
                        "succes":True,
                        "result":result}


api.add_resource(LiveCricketScore, "/live_score")

if __name__=="__main__":
        app.run(host = "0.0.0.0", port = 5000, debug = True)
                
