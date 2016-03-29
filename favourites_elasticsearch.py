#!/usr/bin/env python

import sys
import os
import tornado
import tornado.autoreload
import tornado.ioloop
import tornado.web
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import connection

reload(sys)
sys.setdefaultencoding('utf-8')

es = connection.get_elastic_search_connection()


class GetTeam(tornado.web.RequestHandler):
    """

    """
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
            response.update({'error': False, 'success': True, 'message': 'Success', 'result', res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


class GetLeague(tornado.web.RequestHandler):
    """

    """

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
            response.update({'error': False, 'success': True, 'message': 'Success', 'result', res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)


class GetPlayer(tornado.web.RequestHandler):
    """

    """
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

            response.update({'error': False, 'success': True, 'message': 'Success', 'result', res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)



def make_app():
    return tornado.web.Application([
        (r"/fav_team", GetTeam),
        (r"/fav_league", GetLeague),
        (r"/fav_player", GetPlayer)
    ],
    )


if __name__=='__main__':
    app = make_app()
    app.listen(5000)
    tornado.autoreload.start()
    loop = tornado.ioloop.IOLoop.instance()
    loop.start()
