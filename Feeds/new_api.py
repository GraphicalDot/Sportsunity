#!/usr/bin/env python


import sys
sys.path.append("/home/shivam/programs/wiki-event-sorter/sports-unity/Sportsunity")
from flask import Flask,app,render_template,jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
from DbScripts.mongo_db import CricFeedMongo
from DbScripts.mongo_db_basketball import BasketFeedMongo
from DbScripts.mongo_db_F1 import Formula1FeedMongo
from DbScripts.mongo_db_football import FootFeedMongo
from DbScripts.mongo_db_tennis import TennFeedMongo

app = Flask(__name__)
api = restful.Api(app)


get_args = reqparse.RequestParser()
get_args.add_argument("latest", type=int, location="args")
get_args.add_argument("limited", type=int, location="args")
get_args.add_argument("from", type=float, location="args")
get_args.add_argument("till", type=float, location="args")
get_args.add_argument("image", type=str, location="args")
class Recent_Cricket_News(restful.Resource):
    def get(self):
        args = get_args.parse_args()
        #return CricFeedMongo.recent_news(args)
        if args['latest'] and args['image']:
            return CricFeedMongo.recent_news(args['latest'],args['image'])
        elif args['limited']:
            return CricFeedMongo.number_of_news(args['limited'])
        elif args['from'] and args['till']:
            return CricFeedMongo.news_in_between(args['from'],args['till'])
        else:
            return "Query not entered"

class Recent_Basketball_News(restful.Resource):
    def get(self):
        args = get_args.parse_args()
        if args['latest'] and args['image']:
            return BasketFeedMongo.recent_news(args['latest'],args['image'])
        elif args['limited']:
            return BasketFeedMongo.number_of_news(args['limited'])
        elif args['from'] and args['till']:
            return BasketFeedMongo.news_in_between(args['from'],args['till'])
        else:
            return "Query not entered"

class Recent_F1_News(restful.Resource):
    def get(self):
        args = get_args.parse_args()
        if args['latest'] and args['image']:
            return Formula1FeedMongo.recent_news(args['latest'],args['image'])
        elif args['limited']:
            return Formula1FeedMongo.number_of_news(args['limited'])
        elif args['from'] and args['till']:
            return Formula1FeedMongo.news_in_between(args['from'],args['till'])
        else:
            return "Query not entered"

class Recent_Football_News(restful.Resource):
    def get(self):
        args = get_args.parse_args()
        if args['latest'] and args['image']:
            return FootFeedMongo.recent_news(args['latest'],args['image'])
        elif args['limited']:
            return FootFeedMongo.number_of_news(args['limited'])
        elif args['from'] and args['till']:
            return FootFeedMongo.news_in_between(args['from'],args['till'])
        else:
            return "Query not entered"

class Recent_Tennis_News(restful.Resource):
    def get(self):
        args = get_args.parse_args()
        if args['latest'] and args['image']:
            return TennFeedMongo.recent_news(args['latest'],args['image'])
        elif args['limited']:
            return TennFeedMongo.number_of_news(args['limited'])
        elif args['from'] and args['till']:
            return TennFeedMongo.news_in_between(args['from'],args['till'])
        else :
            return "Query not entered"

            

api.add_resource(Recent_Cricket_News, "/cricket")
api.add_resource(Recent_Basketball_News, "/basketball")
api.add_resource(Recent_F1_News, "/formula1")
api.add_resource(Recent_Football_News, "/football")
api.add_resource(Recent_Tennis_News, "/tennis")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000, debug = True)





