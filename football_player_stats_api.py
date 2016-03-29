#!/usr/bin/env python

import os
import sys
import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web
from pymongo.errors import PyMongoError
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import connection


class GetSquad(tornado.web.RequestHandler):
    """

    """
    def get(self):
        response = {}
        try:
            team_id = self.get_argument('team_id')

            conn = connection.get_mongo_connection()
            football_player_stats_conn = conn.football.football_player_stats

            squad = list(football_player_stats_conn.find({'team_id': team_id}, projection={'_id': False, 'team': True,
                        'team_id': True, 'team': True, 'short_name': True, 'image': True, 'Goals': True,
                        'Assists': True, 'Games': True, 'Nationality': True, 'Position': True, 'Jersey': True,
                        'Age': True, 'Red': True, 'Yellow': True, 'player_id': True}))
            response.update({'error': False, 'success': True, 'data': sorted(squad)})
        except PyMongoError as e:
            response.update({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


class GetPlayerProfile(tornado.web.RequestHandler):
    """

    """
    def get(self):
        response = {}
        try:
            player_id = self.get_argument('player_id')
            conn = connection.get_mongo_connection()
            football_player_stats_conn = conn.football.football_player_stats

            profile = list(football_player_stats_conn.find({'player_id': player_id},projection={'_id': False,
                           'team': True, 'name': True, 'player_id': True, 'player_image': True, 'profile': True,
                           'other_competitions': True}))
            response.update({'error': False, 'success': True, 'data': profile})
        except PyMongoError as e:
            response.update({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


def make_app():
    print 'inside make app'
    return tornado.web.Application([
        (r"/get_football_team_squad", GetSquad),
        (r"/get_football_player_profile", GetPlayerProfile),
    ],
    )


if __name__=='__main__':
    app = make_app()
    app.listen(5600)
    tornado.autoreload.start()
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()
