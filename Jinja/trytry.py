#!usr/bin/env python

import sys
import os
from flask import Flask,app,render_template
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
parent_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print parent_dir_path
sys.path.append(parent_dir_path)
from GlobalConfigs import *
import pymongo


app = Flask(__name__)


class CollectionDetails(restful.Resource):

    @app.route('/collections')
    def get():
        
        number_of_entries = news_collection_ftbl.count()
        print number_of_entries
        for entry in news_collection_ftbl.find(projection={'_id':False}).sort("publish_epoch", -1):
                single_entry_from_collection = entry
                break

                #return single_entry_from_collection
        return render_template("table.html",
                name_of_collection = "SPORTS_UNITY_NEWS_FTBL",
                counts = number_of_entries,
                single_entry = single_entry_from_collection)


    @app.route('/all')
    def get_data():
            collections = [news_collection_cric, news_collection_bask, news_collection_f1rc, news_collection_ftbl, news_collection_tenn]
	    number_of_entries = []
	    single_entry_from_collection = []
            for coll in collections:
		    number_of_entries.append(coll.count())
		    for entry in coll.find(projection={'_id':False, 'news':False}).sort("publish_epoch", -1).limit(1):
                            single_entry_from_collection.append(entry)

	    return render_template("try_table.html",
			    data = zip(collections,number_of_entries,single_entry_from_collection))
			    #name_of_collection = collections,
			    #counts = number_of_entries,
			    #single_entry = single_entry_from_collection)

'''
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
'''


if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 9000, debug = True)




