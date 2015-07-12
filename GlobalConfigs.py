
import pymongo

MONGO_HOST ="localhost"
MONGO_PORT = 27017
MONGO_SPORTS_UNITY_NEWS_DB = "SPORTS_UNITY_NEWS"
MONGO_SPORTS_UNITY_NEWS_CRIC_COLL = "SPORTS_UNITY_NEWS_CRIC"
MONGO_SPORTS_UNITY_NEWS_F1RC_COLL = "SPORTS_UNITY_NEWS_F1RC"
MONGO_SPORTS_UNITY_NEWS_BASK_COLL = "SPORTS_UNITY_NEWS_BASK"
MONGO_SPORTS_UNITY_NEWS_TENN_COLL = "SPORTS_UNITY_NEWS_TENN"
MONGO_SPORTS_UNITY_NEWS_FTBL_COLL = "SPORTS_UNITY_NEWS_FTBL"
MONGO_SPORTS_UNITY_NEWS_ALL_COLL = "SPORTS_UNITY_NEWS_ALL"


AMAZON_ACCESS_KEY = "AKIAJQ4YKSYEDJGYH7ZA"
AMAZON_SECRET_KEY = "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"
S3_BUCKET_NAME = "feeds.images"

connection = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)                                                                                                             

news_collection_cric = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_CRIC_COLL))      

news_collection_f1rc = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_F1RC_COLL))      

news_collection_bask = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_BASK_COLL))      

news_collection_tenn = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_TENN_COLL))      

news_collection_ftbl = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_FTBL_COLL))      

news_collection_all = eval("connection.{db_name}.{collection_name}".format(
          db_name=MONGO_SPORTS_UNITY_NEWS_DB, 
            collection_name=MONGO_SPORTS_UNITY_NEWS_ALL_COLL))      



















