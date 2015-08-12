#!/usr/bin/env python


import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
        def get(self):
                self.write("Hello Motherfucker")


application = tornado.web.Application([\
        (r"/hello",MainHandler),
    ])


if __name__=="__main__":
        application.listen(8888)
        tornado.ioloop.IOLoop.current().start()
