#!usr/bin/env python

import sys
import os
from flask import Flask,app,render_template, make_response
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
parent_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print parent_dir_path
sys.path.append(parent_dir_path)
from GlobalConfigs import *
import pymongo

app = Flask(__name__)
api = restful.Api(app)


class CollectionDetails(restful.Resource):

        def __init__(self):
                super(restful.Resource, self).__init__()

        def get(self):
                self.collection.create_index('publish_epoch')
                number_of_entries = self.collection.count()
                for entry in self.collection.find(projection={'_id':False , 'news':False}).sort("publish_epoch", -1):
                        single_entry_from_collection = entry
                        break
                
                headers = {'Content-Type': 'text/html'}
                #return single_entry_from_collection
                return make_response(render_template("table.html",
                        name_of_collection = self.collection.name,
                        counts = number_of_entries,
			single_entry = single_entry_from_collection),200,headers)
                        #break


class BasketballCollection(CollectionDetails):
        def __init__(self):
                self.collection = news_collection_bask
                super(BasketballCollection,self).__init__()

                

class CricketCollection(CollectionDetails):
        def __init__(self):
                self.collection = news_collection_cric
                super(CricketCollection,self).__init__()

class FootballCollection(CollectionDetails):
        
        def __init__(self):
                self.collection = news_collection_ftbl
                super(FootballCollection,self).__init__()

class FormulaOneCollection(CollectionDetails):

        def __init__(self):
                self.collection = news_collection_f1rc
                super(FormulaOneCollection,self).__init__()
                
class TennisCollection(CollectionDetails):
        
        def __init__(self):
                self.collection = news_collection_tenn
                super(TennisCollection,self).__init__()




        
api.add_resource(BasketballCollection, "/basketballdata")
api.add_resource(CricketCollection, "/cricketdata")
api.add_resource(FootballCollection, "/footballdata")
api.add_resource(FormulaOneCollection, "/formulaonedata")
api.add_resource(TennisCollection, "/tennisdata")



if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 7200, debug = True)




