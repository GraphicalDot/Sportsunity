#!/usr/bin/env python


import pymongo
from pymongo.errors import PyMongoError
from operator import itemgetter
import time
from bson.objectid import ObjectId

class MatchList:

    def __init__(self):

            conn = pymongo.MongoClient()
            db = conn.admin
            db.authenticate('shivam','mama123')
            db = conn.test
            self.test_infoplum_matches = db.test_infoplum_matches
            self.infoplum_match_list = db.infoplum_match_list
            self.live_matches = list()
            self.finished_matches = list()
            self.upcoming_matches = list()
            self.match_list = list()


    def add_matches(self):

            for match in self.test_infoplum_matches.find(projection={'_id':False,'status':True,'match_time':True,'start_date':True,'summary':True}):
                    try:
                        if match['status'] in ['L','P']:
                            self.live_matches.append(match)
                        elif match['status']=='F':
                            self.finished_matches.append(match)
                        else:
                            self.upcoming_matches.append(match)
                    except Exception,e:
                        pass
            
            try:
                self.live_matches = sorted(self.live_matches,key=itemgetter('match_time'))
                self.upcoming_matches = sorted(self.upcoming_matches,key=itemgetter('match_time'))
                self.finished_matches = sorted(self.finished_matches,key=itemgetter('match_time'),reverse=True)
            except Exception,e:
                pass
            print self.upcoming_matches
            print

            #self.match_list.extend(self.upcoming_matches[:4])
            try:
                self.match_list.extend(sorted(self.upcoming_matches,key=itemgetter('match_time'))[:6])
            except:
                pass
            self.match_list.extend(self.live_matches[:])
            #self.match_list.extend(self.finished_matches[:4])
            try:
                self.match_list.extend(sorted(self.finished_matches,key=itemgetter('match_time'),reverse=True)[:4])
            except:
                pass

            print self.match_list

            #for match in self.infoplum_match_list.find():
            print 'here'
            try:
                self.infoplum_match_list.update({'id':1},{'$set':{'id':1,'match_list':self.match_list}},upsert=True)
            except PyMongoError,e:
                print e



if __name__=='__main__':

    obj = MatchList()
    obj.add_matches()


