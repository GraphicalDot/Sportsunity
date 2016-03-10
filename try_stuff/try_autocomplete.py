#!/usr/bin/env python

from elasticsearch import Elasticsearch
from flask import Flask, app, jsonify
from flask.ext import restful
from flask.ext.restful import Api, Resource, reqparse
import requests
import json

app = Flask(__name__)
api = restful.Api(app)

get_args = reqparse.RequestParser()
get_args.add_argument("name", type=str, location="args", required=False)

class GetName(restful.Resource):

    def get(self):
        result = []
        es = Elasticsearch()
        args = get_args.parse_args()
        __body = {'_source': ['name'],'query': {'match_phrase_prefix': {'name': {'autocomplete': {'query': args['name']}}}}}
        __result = es.search(index='my_index',doc_type='my_index',body=__body)

        result = [l["_source"] for l in __result["hits"]["hits"]]

        return {'error':False,
                'success':True,
                'data':result}


api.add_resource(GetName, "/get_name")

if __name__=='__main__':
    app.run(host = "0.0.0.0", port = 5300, debug = True)



