#!/usr/bin/env python

import signal
import tornado
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
from blessings import Terminal
from pymongo.errors import PyMongoError
from tornado.log import enable_pretty_logging
from tornado.web import asynchronous
terminal = Terminal()

import connection
MONGO_CONNECTION = connection.get_mongo_connection()
football_collection = MONGO_CONNECTION.test
football_player_stats_collection = football_collection.football_player_stats


class GetSquad(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = {}
        try:
            team_id = self.get_argument('team_id')
            squad = list(football_player_stats_collection.find({'team_id': team_id}, projection={'_id': False, 'team': True,
                        'team_id': True, 'team': True, 'short_name': True, 'image': True, 'Goals': True,
                        'Assists': True, 'Games': True, 'Nationality': True, 'Position': True, 'Jersey': True,
                        'Age': True, 'Red': True, 'Yellow': True, 'player_id': True}))
            self.write({'error': False, 'success': True, 'data': sorted(squad)})
        except PyMongoError as e:
            self.write({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            self.write({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.finish()
            return


class GetPlayerProfile(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = {}
        try:
            player_id = self.get_argument('player_id')
            profile = list(football_player_stats_collection.find({'player_id': player_id},projection={'_id': False,
                           'team': True, 'name': True, 'player_id': True, 'player_image': True, 'profile': True,
                           'other_competitions': True}))
            self.write({'error': False, 'success': True, 'data': profile})
        except PyMongoError as e:
            self.write({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            self.write({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.finish()
            return


def make_app():
    return tornado.web.Application([
        (r"/get_football_team_squad", GetSquad),
        (r"/get_football_player_profile", GetPlayerProfile),
    ],
    )


def on_shutdown():
    print terminal.red(terminal.bold('Shutting down'))
    tornado.ioloop.IOLoop.instance().stop()
    MONGO_CONNECTION.close()


if __name__=='__main__':
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind("5600")
    enable_pretty_logging()
    http_server.start(30)
    loop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
    loop.start()
