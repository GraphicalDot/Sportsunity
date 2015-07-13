#!/usr/bin/env python


import sys

from flask import Flask,app,render_template,jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
"""
from DbScripts.mongo_db import CricFeedMongo
from DbScripts.mongo_db_basketball import BasketFeedMongo
from DbScripts.mongo_db_F1 import Formula1FeedMongo
from DbScripts.mongo_db_football import FootFeedMongo
from DbScripts.mongo_db_tennis import TennFeedMongo
"""

from GlobalConfigs import news_collection_ftbl 

app = Flask(__name__)
api = restful.Api(app)


get_args = reqparse.RequestParser()
get_args.add_argument("skip", type=int, location="args")
get_args.add_argument("limit", type=int, location="args")
get_args.add_argument("start_date", type=str, location="args", required=False)
get_args.add_argument("end_date", type=str, location="args", required=False)
get_args.add_argument("image_size", type=str, location="args", required=True)

class NewsApi(restful.Resource):
        
        def __init__(self):
            super(restful.Resource, self).__init__()

        def get(self):
                """

                range = (0, '11-7-2015')
                date_time  = "11-7-2015"
                Case 1: When front-end needs only recent news without skip and limit
                    by deafault if not skip and limit present , limit =10, skip=0
                    the required args are 
                                image_size = "ldpi" or "mdpi" or "hdpi"
                                
                Case 2: When front end needs resent news with skip and limit 
                        Args will be 
                                image_size = "ldpi" or "mdpi" or "hdpi"
                                skip : some integer
                                limit: some intger
                Case 3: When front-end needs some news specific to a date 
                        Args will be 
                                image_size = "ldpi" or "mdpi" or "hdpi"
                                start-date: This will be of the format 11-7-2015

                Case 4: When front ends news ranging from some date to some date
                        Args will be :
                                image_size = "ldpi" or "mdpi" or "hdpi"
                                start-date: This will be of the format 11-7-2015
                                end-date: This will be of the format 13-7-2015
                                Make sure the end date is one day ahed , for example if frnt end wants news from 
                                12-7-2015 to 11-7-2015
                                the args will be start_date = 11-7-2015 and end date will be end_date = 13-7-2015
                """
                pattern = '%d-%m-%Y'
                args = get_args.parse_args()
                if not args["limit"]:
                        limit = 10
                if not args["skip"]:
                        skip = 0

                if not args["image_size"] in ["ldpi", "mdpi", "hdpi"]:
                        return {"error":  True, 
                                "success": False, 
                                "error_code": 101, 
                                "messege": "Please send a valid image aize in the argument"
                            }


                projection = {"summary": True, "title": True, "news_id": True, "published": True, "news_link": True, "_id": False}
                projection.update({args["image_size"]: True})
                
                print self.collection, skip, limit, projection
                ##if front end needs news jsut after news with skip and limit 
                if not args["start_date"] and not args["end_date"]:
                        result = self.collection.find(projection=projection).limit(limit).skip(skip).sort("publish_epoch", -1)
                        return {"error":  True, 
                                "success": False, 
                                "result": list(result), 
                                }

                try:
                        start_epoch = int(time.mktime(time.strptime(start_date, pattern)))
                except ValueError as e:
                        return {"error":  True, 
                                "success": False, 
                                "error_code": 102, 
                                "messege": "Please send a valid start date format for the start date in the argument"
                            }
                
                ##This implies that we required news for the present date
                if not end_date:
                        result = self.collection.find({"publish_epoch": {"$gt": start_epoch}}, projection=projection).limit(limit).skip(skip).sort("publish_epoch", -1)
                        return {"error":  True, 
                                "success": False, 
                                "result": list(result)}


                ##this implies that we need news for some date range
                try:
                        end_epoch = int(time.mktime(time.strptime(start_date, pattern)))
                except ValueError as e:
                        return {"error":  True, 
                                "success": False, 
                                "error_code": 102, 
                                "messege": "Please send a valid start date format for the start date in the argument"
                            }
                        
                if end_epoch < start_epoch:
                        return {"error":  True, 
                                "success": False, 
                                "error_code": 103, 
                                "messege": "end date should be greater than start date, Obviously"
                            }
                        

                ##if the news is required for lets say 11-7-2105 to 12-7-2015, end_date should be 13-7-2015
                result = self.collection.find({"publish_epoch": {"$gt": start_epoch, "$lt": end_epoch}}, projection=projection)\
                                                                                    .limit(limit).skip(skip).sort("publish_epoch", -1)
                return {"error":  True, 
                        "success": False, 
                        "result": list(result), 
                        }
                    

class GetFootballNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_ftbl
                super(NewsApi, self).__init__()



class GetCricketNews(restful.Resource):
        def __init__(self):
                self.collection = news_collection_cric
                super(NewsApi, self).__init__()


class GetBasketballNews(restful.Resource):
        def __init__(self):
                self.collection = news_collection_bask
                super(NewsApi, self).__init__()


class GetF1News(restful.Resource):
        def __init__(self):
                self.collection = news_collection_f1rc
                super(NewsApi, self).__init__()


class GetTennisNews(restful.Resource):
        def __init__(self):
                self.collection = news_collection_tenn
                super(NewsApi, self).__init__()

            

api.add_resource(GetFootballNews, "/football")
api.add_resource(GetCricketNews, "/cricket")
api.add_resource(GetBasketballNews, "/basketball")
api.add_resource(GetF1News, "/f1")
api.add_resource(GetTennisNews, "/tennis")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000, debug = True)





