#!/usr/bin/env python


import os
import sys
import smtplib
import feedparser
parent_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print parent_dir_path
sys.path.append(parent_dir_path)
from GlobalLinks import *

class NotifyingRssChanges:

        def __init__(self,url):
                self.mail = smtplib.SMTP('smtp.gmail.com',587)
                self.mail.ehlo()
                self.mail.starttls()
                self.__username = 'shivammutreja25'
                self.__password = 'shivam135'
                self.sender = 'shivammutreja25@gmail.com'
                self.receiver = 'shivam@madmachines.io'
                self.rss = feedparser.parse(url)



        def check_rss(self):
                for entry in self.rss.entries:
                        if entry.has_key('link') or entry.has_key('id') and entry.has_key('published')==True:
                                self.message = list(entry.viewkeys())
                                print self.message
                                return self.message



        
        def send_notification(self):
                self.mail.login(self.__username,self.__password)
                self.mail.sendmail(self.sender,self.receiver,str(self.message))
                self.mail.close()
                print "Mail has been sent"


def main():
        obj = NotifyingRssChanges(Goal_dot_com)
        if obj.check_rss():
                obj.send_notification()


if __name__=='__main__':main()



