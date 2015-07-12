#!/usr/bin/env python

import sys
import os
import urllib2 as urllib
import shutil
from cStringIO import StringIO
from PIL import Image
import PIL
import base64
import requests
file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(file_path)

from GlobalConfigs import S3_BUCKET_NAME, AMAZON_SECRET_KEY, AMAZON_ACCESS_KEY


from boto.s3.connection import S3Connection
from boto.exception import S3ResponseError, S3CreateError


class AmazonS3(object):
        def __init__(self, image_link, news_id):
                self.image_link = image_link
                try:
                    self.image_format = self.image_link.split(".")[-1]
                    if not self.image_format in ["png", "gif"]:
                            raise StandardError("No suitable image format found")
                except Exception as e:
                        print e
                        self.image_format = "png"


                print self.image_format
                self.ldpi_size = (240, 320)
                self.mdpi_size = (320, 480)
                self.hdpi_size = (480, 800)

        def amazon_bucket(self):
                """
                return amazon bucket which will be used to store the images sizes
                """
                try:
                        s3_connection = S3Connection(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY)
                except Exception as e:
                        raise StandardError("The attempt to connect amazon s3 cloud has been failed")

                try:
                        bucket = s3_connection.get_bucket(S3_BUCKET_NAME)
                        
                except S3ResponseError as e:
                        print "The bucket you are trying to connect doesnt exists yet, \
                                Trying to create the bucket required to store the relevant images"
                        bucket = s3_connection.create_bucket(S3_BUCKET_NAME)

                return bucket

        def runn(self):
                try:
                    self.download_image()
                    self.make_resolutions()
                    self.encode_images()
                    return { "ldpi": self.img_ldpi_encoded, 
                            "mdpi": self.img_mdpi_encoded, 
                            "hdpi": self.img_hdpi_encoded, }
                except:
                    return {"ldpi":None,
                            "mdpi":None,
                            "hdpi":None, }

        def download_image(self):
                """
                Download an image from the link
                """
                #response = urllib.urlopen(self.image_link)
                #response = requests.get(self.image_link)
                try:

                    response = urllib.urlopen(self.image_link)
                    self.img = Image.open(StringIO(response.read()))
                except Exception as e:
                    requests.get(self.image_link)
                    self.img = Image.open(StringIO(e.url))
                
                img_ratio = self.img.size[0] / float(self.img.size[1])
                return

        def make_resolutions(self):
                """
                converts the image link to byte 64 encoding
                """
                self.img_ldpi = self.img.resize(self.ldpi_size, Image.ANTIALIAS) 
                self.img_mdpi = self.img.resize(self.mdpi_size, Image.ANTIALIAS) 
                self.img_hdpi = self.img.resize(self.hdpi_size, Image.ANTIALIAS) 
                return 


        def encode_images(self):
                """
                converts the image to different resolutions
                hdpi, mdpi, xdpi
                """
                output = StringIO()
                self.img_ldpi.save(output, self.image_format)
                self.img_ldpi_contents = output.getvalue()
                key = new_id + "_ldpi"
                ldpi_key = self.bucket.new_key(key)
                ldpi_key.set_contents_from_string(output.getvalue()
                ldpi_key.set_canned_acl('public-read')
                self.ldpi_image_url = ldpi_key.generate_url(0, query_auth=False, force_http=True)
                        
                self.img_ldpi_encoded = base64.b64encode(self.img_ldpi_contents)


                output = StringIO()
                self.img_mdpi.save(output, self.image_format)
                self.img_mdpi_contents = output.getvalue()
                self.img_mdpi_encoded = base64.b64encode(self.img_mdpi_contents)
                
                output = StringIO()
                self.img_hdpi.save(output, self.image_format)
                self.img_hdpi_contents = output.getvalue()
                self.img_hdpi_encoded = base64.b64encode(self.img_hdpi_contents)
                return

"""
if __name__ == "__main__":
        i = ImageDownload(image_link="http://a1.espncdn.com/combiner/i?img=/photo/2015/0304/rn_rashangary_ms_1296x518.jpg")
        print i.run()
"""     
