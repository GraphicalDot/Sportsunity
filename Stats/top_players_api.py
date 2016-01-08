#!/usr/bin/env python

from flask import Flask, app, render_template, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
import pymongo

app = Flask(__name__)
api = restful.Api(app)


class TopCricketPlayers(restful.Resource):

    def __init__(self):

        conn = pymongo.MongoClient()
        db = conn.admin
        db.authenticate('shivam','mama123')
        db = conn.cricket
        self.top_cricket_players = db.top_cricket_players

        
    def get(self):

        result = self.top_cricket_players.find(projection={'_id':False})

        return {'error':False,
                'success':True,
                'result':list(result)}


api.add_resource(TopCricketPlayers,'/top_cricket_players')


if __name__=="__main__":
    app.run(host="0.0.0.0",port = 5200, debug = True)



        

