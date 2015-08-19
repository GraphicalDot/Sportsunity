#!/usr/bin/env python


import os
import sys
import pymongo
import requests

class PostRequest:
        def __init__(self):
                conn = pymongo.MongoClient()
                db = conn.drake
                self.testing = db.testing


        def check_new_ball(self):
                ball_by_ball = {}
                check_length = len(ball_by_ball)
                for data in self.testing.find():
                        try:
                                store = data['commentary']
                        except:
                                pass
                for key in store.viewkeys():
                        self.ball_by_ball = store.get(key)
                
                if len(self.ball_by_ball)>check_length:
                        return 'new entry'

        def send_data(self):
                if self.check_new_ball():
                        latest_ball = self.ball_by_ball.items()
                        latest_ball.sort()
                        ball,comment = latest_ball[-1]
                        print {ball:comment}                        
                        
                        """
                        #one could do var = ball_by_ball.iteritems() 
                        #ball,comment in var.next():             
                        #           print {ball:comment}
                        #but there are more than one ',' in comment.
                        #Thus, umpacking the tuple isn't a good idea.
                        """




def main():
        obj = PostRequest()
        #obj.check_new_ball()
        obj.send_data()

if __name__=='__main__':main()

