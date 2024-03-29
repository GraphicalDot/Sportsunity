#!/usr/bin/env python


import sys
import time
from flask import Flask,app,render_template,jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse

#from live_cric_scores import CricketCommentary
from GlobalConfigs import * 
from Elasticsearch_1 import elasticsearch_db
from operator import itemgetter
app = Flask(__name__)
api = restful.Api(app)


get_args = reqparse.RequestParser()
show_args = reqparse.RequestParser()
get_args.add_argument("type_1", location="args", required=False, action='append')
get_args.add_argument("skip", type=int, location="args", required=False)
get_args.add_argument("limit", type=int, location="args", required=False)
get_args.add_argument("start_date", type=str, location="args", required=False)
get_args.add_argument("end_date", type=str, location="args", required=False)
get_args.add_argument("image_size", type=str, location="args", required=True)
get_args.add_argument("news_id", type=str, location="args", required=False)
get_args.add_argument("timestamp", type=int, location="args", required=False)
get_args.add_argument("direction", type=str, location="args", required=False)
get_args.add_argument("search", type=str, location="args", required=False)


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
                        args['limit'] = 10
                if not args["skip"]:
                        args['skip'] = 0

                if not args["image_size"] in ["ldpi", "mdpi", "hdpi", "xhdpi"]:
                        return {"error":  True, 
                                "success": False, 
                                "error_code": 101, 
                                "messege": "Please send a valid image aize in the argument"
                            }

                projection = {"summary": True,"custom_summary":True,"title":True,"website":True, "news_id":\
                        True, "published": True, "publish_epoch": True, "news_link": True, "type": True,'gmt_epoch':True}

                projection.update({args["image_size"]: True, "_id":True, "time_of_storing":True})

                projection.update({"_id": False, "favicon":True,})
                
                if not args['news_id']:
                        pass
                elif args['news_id']:
                        projection.update({"news": True})
                        try:
                                for news in self.collection.find({"news_id":args["news_id"]}, projection=projection).sort("publish_epoch",-1):
                                        result = news

                                result['image_link'] = result.pop(args['image_size'])
                                        
                                return {"error": False,
                                        "success": True,
                                        "result": result,
                                        }
                        except Exception, e:
                                print e
                                return "news_id entered isn't correct"
                

                


                if not args['search']:
                        print 'gfgf'
                    
                        if not args['type_1'] and not args['timestamp'] and not args['direction']:
                                try:
                                        result = self.collection.find(projection=projection).sort('publish_epoch',-1).skip(args['skip']).\
                                                limit(args['limit'])
                                        #result = news

                                        result = list(result)
                                        new_result = []

                                        for val in result:
                                            val['image_link']=val.pop(args['image_size'])
                                            new_result.append(val)

                                        return {"error": False,
                                                "success": True,
                                                "result": list(new_result),
                                                }

                                except Exception, e:
                                    return {"error": True,
                                            "success": False,
                                            "message": "Please send correct sport type",
                                            }
                        elif args['type_1'] and not args['timestamp'] and not args['direction']:
                                try:
                                        print args['type_1']
                                        result = self.collection.find({'type':{'$in':args['type_1']}},projection=projection).sort('publish_epoch',-1)\
                                                .limit(args['limit']).skip(args['skip'])
                                        #result = news

                                        result = list(result)
                                        new_result = []

                                        for val in result:
                                            val['image_link']=val.pop(args['image_size'])
                                            new_result.append(val)

                                        return {"error": False,
                                                "success": True,
                                                "result": list(new_result),
                                                }

                                except Exception, e:
                                        return {"error": True,
                                                "success": False,
                                                "result": result,
                                                }
                


                        #if not args['timestamp'] and not args['direction']:
                        #       pass

                        elif not args['type_1'] and args['timestamp'] and args['direction']:
                                print args['type_1']
                                print args['timestamp']
                                print args['direction']
                                if args['direction']=='up':
                                        print "latest"
                                        try:
                                                result = self.collection.find({'publish_epoch':{"$gt":args['timestamp']}},projection=projection).sort('publish_epoch',-1).limit(args['limit'])
                                                result = list(result)
                                                new_result = []

                                                for val in result:
                                                    val['image_link']=val.pop(args['image_size'])
                                                    new_result.append(val)


                                                return {"error": False,
                                                        "success":True,
                                                        "result":list(new_result),
                                                        }

                                        except Exception,e:

                                                return {"error":False,
                                                        "success":True,
                                                        "result":"No latest news yet",
                                                        }

                                elif args['direction']=='down':
                                        print "older"
                                        try:
                                                result = self.collection.find({"publish_epoch": {"$lt": args['timestamp']}},projection=projection).\
                                                        sort('publish_epoch',-1).skip(args['skip']).limit(args['limit'])

                                        
                                                result = list(result)
                                                new_result = []
                                
                                                for val in result:
                                                    val['image_link']=val.pop(args['image_size'])
                                                    new_result.append(val)

                                                return {"error": False,
                                                        "success": True,
                                                        "result": new_result,
                                                        }

                                        except Exception,e:

                                                return {"error": False,
                                                        "success": True,
                                                        "result" : "This is probably the oldest news we have",
                                                        }

                        elif args['type_1'] and args['timestamp'] and args['direction']:
                                print args['type_1']
                                print args['direction']
                                if args['direction']=='up':
                                        print 'latest'

                                        try:
                                                result = self.collection.find({'type':{'$in':args['type_1']},'publish_epoch':\
                                                        {"$gt":args['timestamp']}},projection=projection).sort('publish_epoch',-1).\
                                                        skip(args['skip']).limit(args['limit'])

                                                result = list(result)
                                                new_result = []

                                                for val in result:
                                                        val['image_link']=val.pop(args['image_size'])
                                                        new_result.append(val)

                                                return {"error": False,
                                                        "success": True,
                                                        "result": new_result,
                                                        }


                                        except Exception,e:
                                        
                                                return {"error": False,
                                                        "success": True,
                                                        "result": "No latest news yet"
                                                        }
                                elif args['direction']=='down':
                                        print "older"
                                        try:
                                                result = self.collection.find({'type':{'$in':args['type_1']},"publish_epoch": {"$lt": args['timestamp']}},\
                                                        projection=projection).sort('publish_epoch',-1).skip(args['skip']).limit(args['limit'])
                                                result = list(result)
                                                new_result = []

                                                for val in result:
                                                        val['image_link']=val.pop(args['image_size'])
                                                        new_result.append(val)

                                                return {"error": False,
                                                        "success": True,
                                                        "result": new_result,
                                                        }

                                        except Exception,e:
                                        
                                                return {"error": False,
                                                        "success": True,
                                                        "result": "This is probably the oldest news",
                                                        }

                                else:
                                        pass
                
                
                elif args['search']:
                        print args['type_1']
                        if not args['timestamp'] and not args['direction']:
                                args['timestamp'] = None
                                args['direction'] = None

                                print 'eeeee'
                                result = elasticsearch_db.ElasticSearchApis.do_query(argument=args['image_size'],text_to_search=args['search'],skip=args['skip'],limit=args['limit'],\
                                        timestamp=args['timestamp'],direction=args['direction'],type_1=args['type_1'])
                                result = sorted(result,key=itemgetter('publish_epoch'),reverse=True)
                                result = result[args['skip']:]
                                new_result = []
                                for val in result:
                                        val['image_link']=val.pop(args['image_size'])
                                        new_result.append(val)
                                
                                return {"error": False,
                                        "success": True,
                                        "result":new_result,
                                        }

                        elif args['timestamp'] and args['direction']:
                                print "pooppooppo"
                                
                                result = elasticsearch_db.ElasticSearchApis.do_query(argument=args['image_size'],text_to_search=args['search'],skip=args['skip'],limit=args['limit'],\
                                        timestamp=args['timestamp'],direction=args['direction'],type_1=args['type_1'])
                                result = sorted(result,key=itemgetter('publish_epoch'),reverse=True)
                                new_result = []
                                for val in result:
                                        val['image_link']=val.pop(args['image_size'])
                                        new_result.append(val)

                                return {"error": False,
                                        "success": True,
                                        "result":new_result,
                                        }

                


                print self.collection, args['skip'], args['limit'], projection

                ##if front end needs news jsut after news with skip and limit 

                if not args["start_date"] and not args["end_date"]:
                        result = self.collection.find(projection=projection).limit(args['limit']).skip(args['skip']).sort("publish_epoch", -1)
                        return {"error":  False, 
                                "success": True, 
                                "result": list(result), 
                                }

                try:
                        start_epoch = int(time.mktime(time.strptime(args['start_date'], pattern)))
                except ValueError as e:
                        return {"error":  False, 
                                "success": True, 
                                "error_code": 102, 
                                "messege": "Please send a valid start date format for the start date in the argument"
                            }
                
                ##This implies that we required news for the present date
                if not args['end_date']:
                        result = self.collection.find({"publish_epoch": {"$gt": start_epoch}}, projection=projection).\
                                limit(args['limit']).skip(args['skip']).sort("publish_epoch", -1)
                        return {"error":  False, 
                                "success": True, 
                                "result": list(result)}


                ##this implies that we need news for some date range
                try:
                        end_epoch = int(time.mktime(time.strptime(args['end_date'], pattern)))
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
                                                                                    .limit(args['limit']).skip(args['skip']).sort("publish_epoch", -1)
                return {"error":  False, 
                        "success": True, 
                        "result": list(result), 
                        }
                    

class GetFootballNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_ftbl
                super(NewsApi, self).__init__()



class GetCricketNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_cric
                super(NewsApi, self).__init__()


class GetBasketballNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_bask
                super(NewsApi, self).__init__()


class GetF1News(NewsApi):
        def __init__(self):
                self.collection = news_collection_f1rc
                super(NewsApi, self).__init__()


class GetTennisNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_tenn
                super(NewsApi, self).__init__()

class GetMixedNews(NewsApi):
        def __init__(self):
                self.collection = news_collection_all
                super(NewsApi, self).__init__()



api.add_resource(GetFootballNews, "/football")
api.add_resource(GetCricketNews, "/cricket")
api.add_resource(GetBasketballNews, "/basketball")
api.add_resource(GetF1News, "/formula1")
api.add_resource(GetTennisNews, "/tennis")
api.add_resource(GetMixedNews, "/mixed")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port = 8000, debug = True)





