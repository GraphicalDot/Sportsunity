#!/usr/bin/env python

import os
import signal
import sys
import tornado
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from blessings import Terminal
from tornado.log import enable_pretty_logging
from tornado.options import options
from newhandlers import GetMixedNews

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import connection
terminal = Terminal()


def make_app():
    print 'inside make app'
    return tornado.web.Application([
        (r"/mixed", GetMixedNews),
    ],
    )

def on_shutdown():
    print terminal.red('Shutting Down')
    tornado.ioloop.IOLoop.instance().stop()

    #gracefully closing mongo connection
    connection.get_mongo_connection().close()


if __name__ == "__main__":
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind(3000)

    options.log_file_prefix = "tornado_log"
    enable_pretty_logging(options=options)

    http_server.start(40)
    tornado.autoreload.start()
    loop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
    loop.start()
