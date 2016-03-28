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
            player_stats_conn = conn.test.player_stats
            squad = list(player_stats_conn.find({'team_id': team_id},projection={'_id': False, 'team_name': True,
                                                'team_id': True, 'player': True, 'player_id': True, 'image': True}))
            response.update({'error': False, 'success': True, 'data': sorted(squad)})
        except PyMongoError as e:
            response.update({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


class GetPlayerStats(tornado.web.RequestHandler):
    """

    """
    def get(self):
        response = {}
        try:
            player_id = self.get_argument('player_id')
            conn = connection.get_mongo_connection()
            player_stats_conn = conn.test.player_stats

            if list(player_stats_conn.find({'player_id': player_id})):
                stats = list(player_stats_conn.find({'player_id': player_id}, projection={'_id': False,
                                                    'team_name': True, 'player': True, 'player_id': True,
                                                    'image': True, 'stats': True, 'info': True}))
                for stat in stats:
                    teams_played_for.setdefault('teams_played_for', []).append(stat['team_name'])

                stats[0].update(teams_played_for)
                stats[0].pop('team_name')
                stats = stats[0]
            else:
                stats = list(player_stats_conn.find({'player_id': player_id}, projection={'_id': False,
                                                    'team_name': True, 'player': True, 'player_id': True,
                                                    'image': True, 'stats': True, 'info': True}))
                teams_played_for.setdefault('teams_played_for',[]).append(stats[0].pop('team_name'))
                stats[0].update(teams_played_for)
                stats = stats[0]

            response.update({'error': False, 'success': True, 'data': stats})
        except PyMongoError as e:
            response.update({'error': True, 'success': False, 'message': 'Database Error: %s' % e})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


def make_app():
    print 'inside make app'
    return tornado.web.Application([
        (r"/get_team_squad", GetSquad),
        (r"/get_player_stats", GetPlayerStats),
    ],
    )


if __name__=='__main__':
    app = make_app()
    app.listen(5400)
    tornado.autoreload.start()
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()
