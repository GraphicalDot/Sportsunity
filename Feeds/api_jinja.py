#!usr/bin/env python

import sys
sys.path.append("/home/shivam/programs/wiki-event-sorter/sports-unity/Sportsunity")
from flask import Flask,app,render_template,jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
from Feeds.Basketball import Inside_hoops_Feed
from Feeds.Basketball import NBA_Feed 
from Feeds.Basketball import Real_gm_Feed
from Feeds.Basketball import Roto_world_Feed 
from GlobalLinks import *
obj = Inside_hoops_Feed.Basketball()

app = Flask(__name__)


class Basketball_News():
    @app.route('/latest_news')
    def get():
        obj.rss_feeds(Inside_hoops)
        obj.checking()
        return obj.reflect_data()




if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8080, debug = True)




