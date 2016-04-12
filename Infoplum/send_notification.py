#!/usr/bin/env python


import os
import sys
import smtplib
from email.mime.text import MIMEText
parent_dir_path = os.path.dirname(os.path.abspath(__file__))
print parent_dir_path
sys.path.append(parent_dir_path)

class NotifyEvent:

        '''
        smtplib is being used to send an email there is any change in
        the keys. Emailing service used is gmail.
        '''

        def __init__(self):
                self.mail = smtplib.SMTP('smtp.gmail.com',587)
                self.mail.ehlo()
                self.mail.starttls()
                self.__username = 'shivammutreja25'
                self.__password = 'ilovepython'
                self.sender = 'shivammutreja25@gmail.com'
                self.receiver = 'shivam@madmachines.io'



        '''
        This method sends an email if check_rss() returns the list of keys
        of a specific rss website, if there is any change in the keys.
        '''
        
        def send_notification(self,notification):
                self.mail.login(self.__username,self.__password)
                self.mail.sendmail(self.sender,self.receiver,str(notification))
                self.mail.close()
                print "Mail has been sent"


def main():
        obj = NotifyEvent()
        obj.send_notification()


if __name__=='__main__':main()


