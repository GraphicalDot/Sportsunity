#!usr/bin/env python

import sys
import os
sys.path.append("/home/shivam/programs/wiki-event-sorter/sports-unity/Sportsunity/Feeds/Basketball")
from flask import Flask,app,render_template
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
from Sportsunity.Feeds.Basketball import Inside_hoops_Feed
from Sportsunity.Feeds.Basketball import NBA_Feed 
from Sportsunity.Feeds.Basketball.Real_gm_Feed import full_news
from Sportsunity.Feeds.Basketball.Roto_world_Feed import full_news



app = Flask(__name__)


class Basketball_News():
    @app.route('/latest_news')
    def get(self):
        return Inside_hoops_feed.full_news




if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8080, debug = True)




