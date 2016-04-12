#!/usr/bin/env python

import sys
import os
import glob
import urllib2 as urllib
import shutil
from cStringIO import StringIO
from PIL import Image
import PIL
import base64
import requests
import goose
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_path)

from GlobalConfigs import S3_BUCKET_NAME, AMAZON_SECRET_KEY, AMAZON_ACCESS_KEY


from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError, S3CreateError


class AmazonS3(object):
        def __init__(self, image_link, player_id):
                self.image_link = image_link
                self.image_format = "png"
                self.player_id = player_id


        def amazon_bucket(self):
                """
                return amazon bucket which will be used to store the images sizes
                """
                try:
                        s3_connection = S3Connection(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY)
                except Exception as e:
                        raise StandardError("The attempt to connect amazon s3 cloud has been failed")

                try:
                        print S3_BUCKET_NAME
                        bucket = s3_connection.get_bucket(S3_BUCKET_NAME)
                        
                except S3ResponseError as e:
                        print "The bucket you are trying to connect doesnt exists yet, \
                                Trying to create the bucket required to store the relevant images"
                        bucket = s3_connection.create_bucket(S3_BUCKET_NAME)

                return bucket

        def run(self):
                    self.bucket = self.amazon_bucket()
                    print self.bucket
                    self.download_image()
                    self.encode_images()
                    return self.image_url 

        def download_image(self):
                """
                Download an image from the link
                """
                try:
                    response = urllib.urlopen(self.image_link)
                    source = response.read()
                    self.img = Image.open(StringIO(source_new))
                except Exception as e:
                    goose_instance = goose.Goose()
                    g = goose_instance.extract(self.image_link)
                    self.img  = Image.open(StringIO(g.raw_html))

                return


        def encode_images(self):
                """
                converts the image to different resolutions
                hdpi, mdpi, xdpi
                """
                output = StringIO()
                self.img.save(output, self.image_format,optimize=True,quality=85)
                self.img_contents = output.getvalue()
                key = self.player_id + ".png"
                image_key = self.bucket.new_key(key)
                image_key.set_metadata('Content-Type', 'image/png')
                image_key.set_contents_from_string(output.getvalue())
                image_key.set_canned_acl('public-read')
                self.image_url = image_key.generate_url(0, query_auth=False, force_http=True)

                return




if __name__ == "__main__":
        i = AmazonS3(image_link='https://i.ytimg.com/vi/oGTbiXEeb_c/hqdefault.jpg', player_id= '2771')
        print i.run()

