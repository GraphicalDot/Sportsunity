#!/usr/bin/env python
#-*- coding: utf-8 -*-

from GlobalConfigs import MONGO_SPORTS_UNITY_NEWS_ALL_COLL, ELASTICSEARCH_IP, TIME_STAMP, SOURCE 
from elasticsearch import Elasticsearch, helpers
from elasticsearch import RequestError
from termcolor import cprint
from pyfiglet import figlet_format 
import time
from blessings import Terminal
#import pyprind
#from tqdm import tqdm

ES_CLIENT = Elasticsearch(ELASTICSEARCH_IP, timeout=30)
terminal = Terminal()


##TODO: Disable scoring on documents: either omit_norms: True in settings for a field or use filtered query
##TODO: Duplicate entries needs to be stopped updating in ELasticsearch, Now, Duplication is meant to be handeled by mongodb effectively

class ElasticSearchSetup(object):
        def __init__(self, renew_indexes=False):
                """
                Index:
                        news:
                                _type: None
                                _type: basketball 
                                _type: cricket 
                                _type: f1 
                                _type: football
                                _type: tennis

                """
                
                self.mappings =  {  "dynamic":      "strict", ##TO ensure that indexing new documents with unwanted keys throws an exception
                                        "properties" : {
                                                "news_autocomplete": { 'analyzer': 'custom_analyzer', 'type': 'string'},   
                                                "custom_summary" : {
                                                            "type" : "string"
                                                            },

                                                "day" : {
                                                            "type" : "long",
                                                            "index":    "not_analyzed",
                                                        },

                                                "mongo_id": {

                                                            "type": "string", 
                                                             "index":    "not_analyzed",
                                                            }, 

                                                "gmt_epoch" : {
                                                            "type" : "long",
                                                            "index":    "not_analyzed",
                                                    },
          
                                                "hdpi" : {
                                                            "type" : "string",
                                                             "index":    "not_analyzed", 
                                                    },
          
                                                "image_link" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed", 
                                                    },
          
                                                "ldpi" : {
                                                        "type" : "string",
                                                        "index":    "not_analyzed",
                                                        },
                                                    
                                                "mdpi" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed", 
                                                        },
          
                                                "month" : {
                                                        "type" : "long",
                                                        "index": "not_analyzed", 
                                                        },

                                                "news" : 
                                                    {'copy_to': ['news_autocomplete'],

                                                        "type" : "string"
                                                        },

                                                "news_id" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                        },

                                                "news_link" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                    },

                                                "publish_epoch" : {
                                                        "type" : "double",
                                                         "index":    "not_analyzed",
                                                    },
                                                
                                                "published" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                    },
          
                                                "summary" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                    },
                                            
                                                "time_of_storing" : {
                                                        "type" : "double",
                                                         "index":    "not_analyzed",
                                                    },
                                                
                                                "title" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                        },

                                                "sport_type" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                        },

                                                "website" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                        },

                                                "favicon": {
                                                        "type": "string",
                                                        "index": "not_analyzed",
                                                        },

                                                "year" : {
                                                        "type" : "long",
                                                         "index":    "not_analyzed",
                                                    }
                                                }
                                }



                self.settings = {'settings':
                                    {'analysis':
                                            {'analyzer':
                                                    {'custom_analyzer': {
                                                                'filter': ['lowercase', 'asciifolding'],
                                                                'tokenizer': 'ngram_tokenizer',
                                                                'type': 'custom'},

                                                        'shingle_analyzer': {
                                                                'filter': ['lowercase', 'asciifolding', 'shingle_tokenizer'],
                                                                'tokenizer': 'ngram_tokenizer',
                                                                'type': 'custom'},

                                                        'keyword_analyzer': {
                                                                    'filter': ['lowercase', 'asciifolding'],
                                                                    'tokenizer': 'keyword',
                                                                    'type': 'custom'},
                                                        },

						
                                                    'filter': {
                                                            'shingle_tokenizer': {'max_shingle_size': 5,
                                                                                    'min_shingle_size': 2,
                                                                                    'type': 'shingle'}
                                                            },
							
                                                    'tokenizer': {
                                                            'limited_tokenizer': {
                                                                        'max_gram': '10',
                                                                        'min_gram': '2',
                                                                        'token_chars': ['letter', 'digit'],
                                                                        'type': 'edgeNGram'},

                                                            'ngram_tokenizer': {'max_gram': 100,
                                                                                'min_gram': 2,
                                                                                'token_chars': ['letter', 'digit'],
                                                                                'type': 'edgeNGram'}
                                                            }
                                                    }
                                                    }
                                        }


                if not ES_CLIENT.indices.exists("news"):
                        self.prep_news_index()

                if renew_indexes:
                        ES_CLIENT.indices.delete(index="news")
                        self.prep_news_index()
                        


        def prep_news_index(self):
                ES_CLIENT.indices.create(index="news", body=self.settings)
                """
                for __sub_category in ['f1', 'cricket', 'basketball', 'None', 'tennis', 'football']:
                                ES_CLIENT.indices.put_mapping(index="news", doc_type=__sub_category, body = {__sub_category: self.mappings })
                                a = "Mappings updated for  {0}".format(__sub_category)
                                cprint(figlet_format(a, font='mini'), attrs=['bold'])   
                """
                ES_CLIENT.indices.put_mapping(index="news", doc_type="news", body = {"news": self.mappings })
                a = "Mappings updated for  {0}".format("news")
                cprint(figlet_format(a, font='starwars'), attrs=['bold'])   
                return 






class ElasticSearchApis(object):
        def __init__(self):
                pass


        def process_result(func):
                """
                Process the result returned, in other words converts the result returned from ES
                into a json which will be used by front end
                """
                def wrapper(*args, **kwargs):
                        __result = func(*args, **kwargs)
                        result = [l["_source"] for l in __result["hits"]["hits"]]
                        return result
                return wrapper

        @staticmethod
        def do_query(image_size, text_to_search, skip, limit, timestamp, direction, type_1):
		"""
                This method of this class first tries to match the exact query searched by the user
                If the original query doesnt returns any results then it tries to call another method 
                called as fuzzy_match, which then tries to find the levenshtien match of the text_to_search

                How this works:
                    Order of searches that will be executed 
                        1. exact match
                        2. promiximity search
                        3. fuzzy search
                        4. token search


                Args:
                        text_to_search: 
                                type: str
                                    The text to be searched
                        skip: 
                                type: int
                                    default: 0
                                    number of news articles to be skipped matching the query, 
                        limit: 
                                type: int 
                                    Default: 10
                                    number of news articles to be returned while querying the database 
                Result:
                        type: list
                            list of articles
                
                
                """

                sport_type = type_1 if type_1 else None
                direction_type = ("gt" if direction == "up" else "lt")  if direction else None


                try:
                        print terminal.on_blue("Trying for excat match")
                        result = ElasticSearchApis.exact_match(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type)          
                except Exception as e:
                        print terminal.red(str(e))


                if not result:
                        print terminal.on_blue("Trying for fuzzy match")
                        try:
                                result = ElasticSearchApis.fuzzy_match(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type)  
                        except Exception as e:
                                print terminal.red(str(e))
                
                if not result:
                        print terminal.on_blue("Trying for token match")
                        try:
                                result = ElasticSearchApis.token_search(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type)
                        except Exception as e:
                                print terminal.red(str(e))
                return result




        @staticmethod
        def exact_match(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type):
                exact_phrase_search_body = { "_source": SOURCE+[image_size],                                                 
                                    "min_score": 0.3,
                                    "query": {
                                            "filtered": {
                                                    "query":  { "match_phrase": { "news_autocomplete": text_to_search }},
                                                    "filter": {
                                                        "bool": {
                                                             "must": [
                                                                    {"term": { "sport_type": sport_type }},
                                                                    {"range": {"publish_epoch": {
                                                                                direction_type: timestamp
                                                             }}}]
                                                        }
                                                        }
                                                    }
                                                         },
                                    "sort": { "publish_epoch": { "order": "desc" }},
                                    "from": skip, 
                                    "size": limit, 
                                    }
                return ElasticSearchApis.get_result(exact_phrase_search_body, timestamp, direction_type, sport_type)


        
        @staticmethod
        def token_search(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type):
                token_search_body = { "_source": SOURCE+[image_size],                                                 
                                    "min_score": 0.3,
                                    "query": {
                                            "filtered": {
                                                    "query":  { "match": { "news_autocomplete": 
                                                         {"query":    text_to_search,
                                                         "operator": "and"
                                                        }
                                                        
                                                        }},
                                                    "filter": {
                                                        "bool": {
                                                             "must": [
                                                                    {"term": { "sport_type": sport_type}},
                                                                    {"range": {"publish_epoch": {
                                                                                direction_type: timestamp
                                                             }}}]
                                                        }
                                                        }
                                                    }
                                                         },
                                    "sort": { "publish_epoch": { "order": "desc" }},
                                    "from": skip, 
                                    "size": limit, 
                                    }

                return ElasticSearchApis.get_result(token_search_body, timestamp, direction_type, sport_type)


        @staticmethod
        def fuzzy_match(image_size, text_to_search, skip, limit, timestamp, direction_type, sport_type):
                fuzzy_search_body = { "_source": SOURCE+[image_size],                                                 
                                    "min_score": 0.3,
                                    "query": {
                                            "filtered": {
                                                    "query":  { "match": { "news_autocomplete": 
                                                         {"query":    text_to_search,
                                                            "fuzziness": "AUTO",
                                                         "operator": "and"
                                                        }
                                                        
                                                        }},
                                                    "filter": {
                                                        "bool": {
                                                             "must": [
                                                                    {"term": { "sport_type": sport_type}},
                                                                    {"range": {"publish_epoch": {
                                                                                direction_type: timestamp
                                                             }}}]
                                                        }
                                                        }
                                                    }
                                                         },
                                    "sort": { "publish_epoch": { "order": "desc" }},
                                    "from": skip, 
                                    "size": limit, 
                                    }

                return ElasticSearchApis.get_result(fuzzy_search_body, timestamp, direction_type, sport_type)
		
        @staticmethod
        @process_result
        def get_result(query, timestamp, direction_type, sport_type):
                start = time.time()
                if not any([direction_type, timestamp, sport_type]):
                        """
                        if all three are false
                        """
                        query["query"]["filtered"].pop("filter")

                if not any([direction_type, timestamp]):
                        query["query"]["filtered"]["filter"]["bool"]["must"].pop(-1)
                
                print terminal.on_red("Total time taken for exact match query to return is %s seconds"%(time.time() - start))
                result = ES_CLIENT.search(index="news", doc_type="news", body=query)
                return result
                        


                

class PopulateElasticSearch(object):
        def __init__(self):

                self.last_epoch = self.get_last_epoch()
                if not self.last_epoch:
                        cprint(figlet_format("No document exists in mongodb, STARTING FRESH :) ", font='mini'), attrs=['bold'])
                        
                self.articles = self.fetch_articles_mongo()

                if not self.articles:
                        cprint(figlet_format("No new documents beeds to updated to elastic search", font='mini'), attrs=['bold'])
                else:
                        self.feed_elasticsearch()
                return 

        
        def get_last_epoch(self):
                """
                Get the last sorted epoch time from the elasticsearch which will be the last latest news populated into elasticsearch
                This will be used to get the news articles that will be stored in mongodb after this epoch
                """
                ES_CLIENT.indices.refresh(index="news")
                time.sleep(5)
                __all = {'query': 
                            {'filtered': {
                                        'query': {
                                                    'match_all': {}
                                                    }
                                        }
                            }, 
                            '_source': ['publish_epoch'], 
                            "sort": [
                                    {"publish_epoch": 
                                        {"order": "desc"}
                                        } 
                                    ], 
                            "from": 0, 
                            "size": 2}


                __result = ES_CLIENT.search(index="news", doc_type="news", body=__all)
                print __result
                
                try:
                        last_epoch = [l["_source"] for l in __result["hits"]["hits"]][0]["publish_epoch"]
                except IndexError:
                        last_epoch = 0

                return last_epoch


        def fetch_articles_mongo(self):
                """
                Get the last epoch from self.get_last_epoch adn get the news from mongo which was stored after this epoch in 
                mongodb

                """
                all_articles = list(MONGO_SPORTS_UNITY_NEWS_ALL_COLL.find({TIME_STAMP: {"$gt": self.last_epoch}}))
                return  all_articles


        def feed_elasticsearch(self):
                """
                Populate elasticsearch with articles returned from fetch_articles_mongo
                """
                import time
                import sys

                toolbar_width = 100

                # setup toolbar
                sys.stdout.write("[%s]" % (" " * toolbar_width))
                sys.stdout.flush()
                sys.stdout.write("\b" * (toolbar_width+1))
                error_list = list()
                total_length = len(self.articles)
                length = len(self.articles)/100


                size = 0
                start = time.time()
                for (i, news_article)  in enumerate(self.articles):
                            _id = news_article.pop("_id")
                            sport_type = news_article.pop("type")
                            news_article.update({"mongo_id": str(_id), "sport_type": sport_type })
                            try:
                                    ES_CLIENT.index(index="news", doc_type="news", body=news_article)
                            except Exception as e:
                                    
                                    error_list.append(news_article.get("news_id"))
                                    pass 
                            if i%length == 0:
                                size += 1
                                sys.stdout.write("\r%s[%s%s] %i/%i \b Errors: %s \b Percentage completion:  %s" % ("Updating", "#"*size, "."*(100-size), i, total_length, len(error_list), float(i)/total_length *100))
                                sys.stdout.flush()
                            sys.stdout.write("\r%s[%s%s] %i/%i \b Errors: %s \b Percentage completion:  %s" % ("Updating", "#"*size, "."*(100-size), i, total_length, len(error_list), float(i)/total_length *100))
                            sys.stdout.flush()
                
                print error_list

                ES_CLIENT.indices.refresh(index="news")
                return 



	def if_document_exists(self, mongo_object_id):
		
            
            
                body={
                        "query":{
                                "term":{       
                                        "mongo_id":   str(mongo_object_id), 
                                                }
                                        },
                             }


                ES_CLIENT.search(index="news", doc_type="news", body=body)

                return 



if __name__ == "__main__":
        
        ElasticSearchSetup(renew_indexes=True)
        PopulateElasticSearch()
        #print ElasticSearchApis.do_query(argument='hdpi',text_to_search="johnsan")
        #print SOURCE












