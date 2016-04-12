#!/usr/bin/env python
#*--encoding: utf-8 --*

#    visióna
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
from tornado.web import asynchronous
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
terminal = Terminal()

import connection

reload(sys)
sys.setdefaultencoding('utf-8')

es = connection.get_elastic_search_connection()

class GetTeam(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = {}
        try:
            team = self.get_argument('team')
            sport_type = self.get_argument('sport_type')

            body = {
                "_source": ['team_name','team_id','flag_image'],
                "query": {
                    "and": [ { "match_phrase" :{ "team_autocomplete": {"query": team,"fuzziness": 10,"operator": "and"}}},
                             {'match': {'sport_type': sport_type}}
                             ]
                }
            }

            result = es.search(index='teams', doc_type='teams', body=body)
            res = [l["_source"] for l in result["hits"]["hits"]]
            response.update({'error': False, 'success': True, 'message': 'Success', 'result': res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)
            self.finish()
            return


class GetLeague(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = {}
        try:
            league = self.get_argument('league')
            body = {
                "_source": ['league_name','league_id'],
                "query": {
                    "match_phrase" : {
                        "league_autocomplete": {
                            "query": league,
                            "fuzziness": 10,
                            "operator": "and"
                        }
                    }
                }
            }
            result = es.search(index='leagues', doc_type='leagues', body=body)
            res = [l["_source"] for l in result["hits"]["hits"]]
            response.update({'error': False, 'success': True, 'message': 'Success', 'result': res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)
            self.finish()
            return


class GetPlayer(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = {}
        try:
            player = self.get_argument('player')
            sport_type = self.get_argument('sport_type')
            body = {
                "_source": ['name','player_id','player_image'],
                "query": {
                    "and":[
                        { "match_phrase_prefix" : {
                            "name": {
                                "query": player,
                                "fuzziness": 10,
                                "operator": "and"
                            }
                        }
                        },
                        { "match" : {
                            "sport_type": sport_type
                        }
                        }
                    ]
                }}
            result = es.search(index='players', doc_type='players', body=body)
            res = [l["_source"] for l in result["hits"]["hits"]]

            response.update({'error': False, 'success': True, 'message': 'Success', 'result': res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)
            self.finish()
            return


def make_app():
    return tornado.web.Application([
        (r"/fav_team", GetTeam),
        (r"/fav_league", GetLeague),
        (r"/fav_player", GetPlayer)
    ],
    )


def on_shutdown():
    print terminal.red(terminal.bold('Shutting down'))
    tornado.ioloop.IOLoop.instance().stop()


if __name__=='__main__':
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind("5000")
    enable_pretty_logging()
    http_server.start(20)
    loop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
    loop.start()
