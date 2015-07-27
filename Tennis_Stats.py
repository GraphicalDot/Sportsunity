#!/usr/bin/env python

import os
import sys
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print parent_dir_path
import json
import pymongo


def get_stats():
        conn = pymongo.MongoClient()
        db = conn.drake
        tennis = db.tennis
        f = open("Data_Set_Tennis.json","rb")
        data = f.read()
        stats = json.loads(data)
        for x in stats['data']:
                try:
                        tennis.insert({"Name":x['name'][0].encode('ascii','ignore'), "Ranking":x['singles_ranking'][0], "Country": \
                                x['country'][0].encode('ascii','ignore'), "Gender": x['gender'][0].encode('ascii','ignore'), "Birthdate": \
                                x['birthday/_source'][0].encode('ascii','ignore'), "Matches_Lost_This_Year":x['year_matches_lost'][0]})
                except:
                        tennis.insert({"Name":x['name'][0].encode('ascii','ignore'), "Ranking":x['singles_ranking'][0], "Country": \
                                x['_source'][0].encode('ascii','ignore'), "Gender": x['gender'][0].encode('ascii','ignore'), "Birthdate": \
                                x['birthday/_source'][0].encode('ascii','ignore'), "Matches_Lost_This_Year":x['year_matches_lost'][0]})

def check_data():
        conn = pymongo.MongoClient()
        db = conn.drake
        tennis = db.tennis
        for val in tennis.find(projection={"_id":False}):
                if len(val['Country'])>10:
                        tennis.remove(val)
                        print "removed"
                else:
                        pass


                

if __name__=="__main__":
        get_stats()
        check_data()

