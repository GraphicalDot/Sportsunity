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
                "_source": ['team_name','team_id','team_flag'],
                "query": {
                    "and": [ { "match_phrase" :{ "team_autocomplete": {"query": team,"fuzziness": 10,"operator": "and"}}},
                             {'match': {'sport_type': sport_type}}
                             ]
                }
            }

            result = es.search(index='teams', doc_type='teams', body=body)
            res = [l["_source"] for l in result["hits"]["hits"]]
            response.update({'error': False, 'success': True, 'message': 'Success', 'data': res})
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
                "_source": ['league_name','league_id', 'region'],
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
            response.update({'error': False, 'success': True, 'message': 'Success', 'data': res})
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

            response.update({'error': False, 'success': True, 'message': 'Success', 'data': res})
        except Exception as e:
            response.update({'error': True, 'success': False, 'message': 'Error: %s' % e})
        finally:
            self.write(response)
            self.finish()
            return

class GetAll(tornado.web.RequestHandler):
      """
    
      """
      @asynchronous
      @tornado.gen.coroutine
      def get(self):
        all_search_types = ['news', 'team', 'match', 'league', 'player']
        response = {}
        try:
            search = self.get_argument('search')
            sport_type = self.get_arguments('sport_type', strip=True)
            search_type = self.get_arguments('search_type', strip=True)
            if 'all' in search_type:
                search_type = all_search_types
            if not sport_type:
                sport_type = ['cricket', 'football']
            body = {
                "_source": ['name','id','image', 'region', 'sport_type', 'search_type', 'series_id', 'home_team', 'away_team', 'result', 'status', 'summary', 'title', 'publish_epoch', 'favicon',\
                            'home_team_flag', 'away_team_flag', 'news_link', 'match_widget', 'venue', 'home_team_short_name', 'away_team_short_name', 'match_number', 'away_team_score', 'home_team_score', 'timer'],
                "query": {
                    'filtered':{
                        'query':{
                            "multi_match": {
                            #"match_phrase_prefix" : {
                                #"name": {
                                "query": search,
                                "fuzziness": 10,
                                "operator": "and",
                                "fields": ["name^3", "home_team", "away_team", "title^2"],
                                "type": "most_fields",
                                "analyzer":   "standard"
                                        }
                                },#},
                        "filter": {
                            "terms": {
                                "sport_type": sport_type},
                            "terms": {
                                "search_type": search_type,
                                    }
                                }
                            }
                        },
                "sort": { "publish_epoch": { "order": "desc" }},
                "size": 80
                    }

            result = es.search(index='all', doc_type='all', body=body)
            res = [l["_source"] for l in result["hits"]["hits"]]

            new_res = {}

            for item in res:
                new_res.setdefault(item['search_type'], list()).append(item)
            if res:
                for key in all_search_types:
                    if key not in new_res.keys():
                        new_res.update({key: list()})
            else:
                for val in search_type:
                    new_res.update({val: list()})

            if search_type == all_search_types:
                for new_key in new_res:
                    new_res.update({new_key: new_res.get(new_key,[])[:2]})

            response.update({'error': False, 'success': True, 'message': 'Success', 'data': new_res})
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
        (r"/fav_player", GetPlayer),
        (r"/fav_anything", GetAll)
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
