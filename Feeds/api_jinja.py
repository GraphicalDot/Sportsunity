#!usr/bin/env python

import sys
sys.path.append("/home/shivam/programs/wiki-event-sorter/sports-unity/Sportsunity")
from flask import Flask,app,render_template,jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
#from Feeds.Basketball import Inside_hoops_Feed
#from Feeds.Basketball import NBA_Feed 
#from Feeds.Basketball import Real_gm_Feed
#from Feeds.Basketball import Roto_world_Feed 
#from GlobalLinks import *
from Run_Feeds import run_basketball_rss, run_cricket_rss, run_f1_rss, run_football_rss, run_tennis_rss
#obj = Inside_hoops_Feed.Basketball()

app = Flask(__name__)


class Basketball_News():
    @app.route('/basketball')
    def get():
        #obj.rss_feeds(Inside_hoops)
        #obj.checking()
        #return obj.reflect_data()
        return run_basketball_rss()

class Cricket_News():
    @app.route('/cricket')
    def get_cric():
        return run_cricket_rss()

class F1_News():
    @app.route('/formula_one')
    def get_f1():
        return run_f1_rss()

class Football_News():
    @app.route('/football')
    def get_foot():
        return run_football_rss()

class Tennis_News():
    @app.route('/tennis')
    def get_tenn():
        return run_tennis_rss()



if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8080, debug = True)




