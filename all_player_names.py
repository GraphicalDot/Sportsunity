#!/usr/bin/env python

import signal
import tornado
import tornado.autoreload
import tornado.httpserver
import tornado.ioloop
import tornado.web
import connection
from blessings import Terminal
from pymongo.errors import PyMongoError
from tornado.log import enable_pretty_logging
from tornado.web import asynchronous
terminal = Terminal()

MONGO_CONNECTION  = connection.get_mongo_connection()
football_player_stats_collection = MONGO_CONNECTION.football.player_stats
players_collection = MONGO_CONNECTION.cricket.players

class GetPlayerNames(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        try:
            cricket_players = list(players_collection.find({},{'_id': False, 'team_name': True, 'name': True,
                                                                 'player_id': True, 'sport_type': True}))
            football_players = list(football_player_stats_collection.find({},{'_id': False, 'name': True,
                                                                                'player_id': True, 'sport_type': True}))

            self.write({'success': True, 'error': False, 'data': cricket_players + football_players})
        except Exception as e:
            self.write({'success': False, 'error': True, 'message': 'Error: %s' % e})
        finally:
            self.finish()
            return


class GetAllCricketTeams(tornado.web.RequestHandler):
    """

    """
    @asynchronous
    @tornado.gen.coroutine
    def get(self):
        teams_list = []
        team_ids_list = []
        try:
            players_collection = MONGO_CONNECTION.cricket.players
            for player in players_collection.find({},{'_id': False, 'team': True, 'team_id': True}):
                if player['team_id'] not in team_ids_list:
                    teams_list.append({'team_name': player['team'], 'team_id': player['team_id']})
                    team_ids_list.append(player['team_id'])

            self.write({'success': True, 'error': False, 'data': teams_list})
        except Exception as e:
            self.write({'success': False, 'error': True, 'message': 'Error: %s' % e})
        finally:
            self.finish()
            return


def make_app():
    return tornado.web.Application([
        (r"/get_player_names", GetPlayerNames),
        (r"/get_cricket_teams", GetAllCricketTeams),
    ],
    )


def on_shutdown():
    print terminal.red(terminal.bold('Shutting down'))
    tornado.ioloop.IOLoop.instance().stop()
    MONGO_CONNECTION.close()        ##gracefully closing mongo connection


if __name__=='__main__':
    app = make_app()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.bind("6900")
    enable_pretty_logging()
    #MONGO_CONNECTION  = connection.get_mongo_connection()
    #football_player_stats_collection = MONGO_CONNECTION.football.player_stats
    #players_collection = MONGO_CONNECTION.cricket.players
    http_server.start(10)
    loop = tornado.ioloop.IOLoop.instance()
    signal.signal(signal.SIGINT, lambda sig, frame: loop.add_callback_from_signal(on_shutdown))
    loop.start()
