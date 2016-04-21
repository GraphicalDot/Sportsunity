import os
import pymongo
import settings
from elasticsearch import Elasticsearch

elastic_search_conn = None

def get_elastic_search_connection():
    """
    :return: connection to elastic search server.
    """
    global elastic_search_conn
    if not elastic_search_conn:
        elastic_search_conn = Elasticsearch(settings.ELASTIC_SERVER, timeout=30, maxsize=50) \
            if os.getlogin() == 'ubuntu' else Elasticsearch()
    return elastic_search_conn


def get_mongo_connection():
    """
    :return: connection to mongo server.
    """
    from gevent import monkey
    monkey.patch_all()
    connection = pymongo.MongoClient(settings.MONGO_SERVERIP, settings.MONGO_PORT) \
        if os.getlogin() == 'ubuntu' else pymongo.MongoClient()
    return connection
