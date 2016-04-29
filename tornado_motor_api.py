#!/usr/bin/env python

import sys
import time
import motor
import pymongo
#from live_cric_scores import CricketCommentary
from GlobalConfigs import * 
from Elasticsearch_1 import elasticsearch_db
from operator import itemgetter
from blessings import Terminal
import signal
import connection
from GlobalConfigs import MONGO_SPORTS_UNITY_NEWS_DB, MONGO_SPORTS_UNITY_NEWS_ALL_COLL
import settings
import tornado
import tornado.ioloop
import tornado.web
import tornado.autoreload
from tornado.httpclient import AsyncHTTPClient
from tornado.log import enable_pretty_logging
import shutil
import tornado.httpserver
from itertools import ifilter
from tornado.web import asynchronous
from tornado.concurrent import run_on_executor
terminal = Terminal()


"""
http://localhost:8888/testapi?&image_size=hdpi&limit=10&type_1=cricket
http://localhost:8888/testapi?image_size=hdpi&limit=10&timestamp=1447739320&direction=up

"""

#client = motor.MotorClient()
#db = client.SPORTS_UNITY_NEWS
#collection = db.SPORTS_UNITY_NEWS_ALL

#MONGO_CONNECTION  = connection.get_mongo_connection()
#collection = MONGO_CONNECTION[MONGO_SPORTS_UNITY_NEWS_DB][MONGO_SPORTS_UNITY_NEWS_ALL_COLL]
"""
try:
        #db = app.settings.db
        db.collection.index_information()["type_1"]
        print terminal.on_blue("INdex on type exists")
except Exception as e:
        db.collection.create_index("type")

try:
        app.settings.collection.index_information()["publish_epoch_1"]
        app.settings.collection.drop_index("publish_epoch_1")
except Exception as e:
        app.settings.collection.create_index([('publish_epoch', pymongo.DESCENDING)])
        print terminal.on_blue("INdex on publish epoch created")
"""

class NewsApiTornado(tornado.web.RequestHandler):
        
        def initialize(self):
                db = self.settings['db']
                self.collection = db.SPORTS_UNITY_NEWS_ALL
                try:
                    self.collection.index_information()["type_1"]
                    print terminal.on_blue("INdex on type exists")
                except Exception,e:
                    self.collection.create_index("type")
                try:
                    self.collection.index_information()["publish_epoch_1"]
                    self.collection.drop_index("publish_epoch_1")
                except Exception,e:
                    self.collection.create_index([('publish_epoch', pymongo.DESCENDING)])
                    print terminal.on_blue("INdex on publish epoch created") 
                self.set_status(200)

    
        @asynchronous
        @tornado.gen.coroutine
        def get(self):
                self.limit = int(self.get_argument('limit', 10))
                self.skip = int(self.get_argument('skip', 0))
                self.image_size = self.get_argument('image_size', None)
                self.timestamp = self.get_argument("timestamp", None)
                self.direction = self.get_argument("direction", None)
                self.search = self.get_argument("search", None)
                self.type_1 = self.get_arguments("type_1",strip=True)
                self.success = {"error": False, "success": True, "result": None}
                self.error = {"error": True, "success": False, "messege": None, "status": None}
                self.news_id = self.get_argument("news_id", None)
                
                
                
                if self.image_size not in ["ldpi", "mdpi", "hdpi", "xhdpi"]:
                        self.clear()
                        self.set_status(400)
                        self.error.update({"message": 'Bad Request: Invalid Image size!', "status": 400})
                        self.write(self.error)
                        self.finish()
                        return
                
                self.projection = { "summary": True, "custom_summary": True, "title": True, "website": True, "news_id": True,
                                "published": True, "publish_epoch": True, "news_link": True, "type": True, "gmt_epoch":True,
                                self.image_size: True, "_id": False, "time_of_storing": True, "favicon":True, self.get_argument("image_size"): True}


                if self.news_id:
                        self.projection.update({"news": True})
                        try:
                                cursor = self.collection.find_one({"news_id": self.news_id}, self.projection)#projection=self.projection)
                                docs = yield cursor
                                docs['image_link'] = ([docs][0].pop(self.image_size))
                                #result["image_link"] = result.pop(self.image_size)
				self.success.update({"result": docs})
                                self.write(self.success)
                        except Exception, e:
                                print terminal.on_red(str(e))
                                self.error.update({"message": str(e), "status": 400})
                                self.write(self.error)
                                
                        return 


                if not self.search:
                        query = {}
                        if self.type_1:
                                query.update({'sport_type':{'$in':self.type_1}})
                                print query

                        if self.timestamp and self.direction:
                                print self.direction, self.timestamp
                                query.update({'publish_epoch':{"$gt": int(self.timestamp)}}) if self.direction == "up" else \
						query.update({'publish_epoch':{"$lt": int(self.timestamp)}})

                                print query
                        try:
                                cursor = self.collection.find(query, self.projection).sort('publish_epoch',-1).limit(self.limit).skip(self.skip)
                                docs = yield cursor.to_list(None)
                                new_list = list()
				for post in docs:
                                	post["image_link"] = post.pop(self.image_size)
					new_list.append(post)


				self.write({"error": False,
                                    "success": True,
                                    "result": new_list,
                                    })

                        except Exception as e:
                                print terminal.on_red(str(e))
                                self.set_status(500)
                                self.write({
                                    'message': str(e),
                                    'error': True,
                                    'success': False,
                                    })
                                

                
                if self.search:
                    
			result = elasticsearch_db.ElasticSearchApis.do_query(image_size=self.image_size, text_to_search=self.search, skip=self.skip, limit=self.limit,\
                                        timestamp=int(self.timestamp) if self.timestamp else None, 
					direction=self.direction, type_1=self.type_1)
                        result = sorted(result,key=itemgetter('publish_epoch'),reverse=True)
                        
                        result = result[self.skip:]
                        ##Instead of using a loop to find image link for image siz, get documents from source form elasticsearch 
                        self.write({"error": False,
                                        "success": True,
                                        "result":result,
                                        })
                self.finish()
                return 
                    

app = tornado.web.Application([
                    (r"/mixed", NewsApiTornado),
                    ])





def graceful_reload(signum, traceback):
        """Explicitly close some global MongoClient object."""
        #client.close()
        #signal.signal(signal.SIGHUP, graceful_reload)




def on_shutdown():
        print terminal.red(terminal.bold('Shutting down'))
        tornado.ioloop.IOLoop.instance().stop()
        ##gracefully closing mongo connection
        #MONGO_CONNECTION.close()
        client.close()


def main():
        http_server = tornado.httpserver.HTTPServer(app)
        http_server.bind("8000")
        enable_pretty_logging()
        http_server.start(30)
        client = motor.MotorClient()
        db = client.SPORTS_UNITY_NEWS
        app.settings['db'] = db
        loop = tornado.ioloop.IOLoop.instance()
        signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
        loop.start()

if __name__ == '__main__':
        print 'Server Reloaded'
        main()

