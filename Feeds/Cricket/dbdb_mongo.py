#!/usr/bin/env python


import pymongo

conn = pymongo.MongoClient()
db = conn.Cricket_db
Unity_Cricket = db.Unity_Cricket

class Data_Management:
    @staticmethod
    def Storing(data):
        Unity_Cricket.insert(data)

    @staticmethod
    def Checking_Rss(args):
        if Unity_Cricket.find_one({'News_Id': args}, fields = {'_id':False}):
            return True
        return False





