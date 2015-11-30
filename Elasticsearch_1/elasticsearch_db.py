#!/usr/bin/env python
#-*- coding: utf-8 -*-

from GlobalConfigs import MONGO_SPORTS_UNITY_NEWS_ALL_COLL, ELASTICSEARCH_IP, TIME_STAMP, SOURCE 
from elasticsearch import Elasticsearch, helpers
from elasticsearch import RequestError
from termcolor import cprint
from pyfiglet import figlet_format 
import time


ES_CLIENT = Elasticsearch(ELASTICSEARCH_IP, timeout=30)


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

                                                "type" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
                                                        },

                                                "website" : {
                                                        "type" : "string",
                                                         "index":    "not_analyzed",
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
                cprint(figlet_format(a, font='mini'), attrs=['bold'])   
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
        def do_query(text_to_search, skip=0, limit=10):
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
                result = ElasticSearchApis.exact_match(text_to_search, skip, limit)          
                if not result:
                        result = ElasticSearchApis.proximity_search(text_to_search, skip, limit)          
                        
                
                if not result:
                        result = ElasticSearchApis.fuzzy_match(text_to_search, skip, limit)          
                
                if not result:
                        result = ElasticSearchApis.token_search(text_to_search, skip, limit)          
                return result




        @staticmethod
        @process_result
        def exact_match(text_to_search, skip=0, limit=10):
                """
                Searches fr the exact result in the data 
                """
	        exact_phrase_search_body = {
                            "_source": SOURCE,
                            "query": {
                                    "match_phrase": {
                                            "news_autocomplete": {
                                                    "query":    text_to_search,
                                                            }
                                                }
                                        },
                            "from": skip, 
                            "size": limit, 
                             }

                result = ES_CLIENT.search(index="news", doc_type="news", body=exact_phrase_search_body)
                return result

        
        @staticmethod
        @process_result
        def token_search(text_to_search, skip=0, limit=10):
                """
                It will work as follows
                    if text_to_search = "chelsea midfield"
				matches for articles that have both chelsea and midfield

                """
        
                token_search_body = {                                                 
                                "_source": SOURCE,
                                "query": {
                                        "match": {
                                                "news_autocomplete": {
                                                        "query":    text_to_search,
                                                        "operator": "and"
                                                                    }
                                                }
                                        },
                                
                                "from": skip,
                                "size": limit,
                                }



                result = ES_CLIENT.search(index="news", doc_type="news", body=token_search_body)
                return result




        @staticmethod
        @process_result
        def proximity_search(text_to_search, skip=0, limit=10):
                """
                Sometimes a phrase match can be too restrictive. What if we’re not really interested in a precise match, but we’d rather 
                retrieve documents where the query terms occur somehow close to each other. This is an example of proximity search: the 
                order of the terms doesn’t really matter, as long as they occur somehow within the same context. This concept is less 
                restrictive than a pure phrase match, but still stronger than a general purpose query.
                
                
                So, this will work as follows
                    if text_to_search - "chelsea rui faria"
                    it will search all the three terms in the whole article whether all the three terms in same sentence or in different sentence
                """

                proximity_search_body = {
                        "_source": SOURCE,         
                        "query": {
                                "match_phrase": {
                                        "news_autocomplete": {
                                                "query": text_to_search,
                                                "slop": 10000
                                                }
                                },
                        "from": skip,
                        "size": limit,
                            }
                                    }

                result = ES_CLIENT.search(index="news", doc_type="news", body=proximity_search_body)
                return result




        @staticmethod
        @process_result
        def fuzzy_match(text_to_search, skip=0, limit=10):
                """
                Matches text to search on the basis of levenshtein algorithm
                Args:
                        text_to_search: 
                                type: str
                                    The text to be searched
                        skip: 
                                type: int
                                    number of news articles to be skipped matching the query, 
                        limit: 
                                type: int 
                                    number of news articles to be returned while querying the database 

                Returns:
                        type: list
                            List of articles satisfying the query withfields mentioned in SOURCE
                """

                fuzzy_search_body = {
                            "_source": SOURCE,
                            "query": {
                                    "match": {
                                        "news_autocomplete": {
                                                    "query":     text_to_search,
                                                    "fuzziness": 10,
                                                    "operator":  "and"
                                        }
                                            }
                                },
                            "from": skip, 
                            "size": limit,
                      }


                result = ES_CLIENT.search(index="news", doc_type="news", body=fuzzy_search_body)

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
                for news_article  in self.articles:
                            _id = news_article.pop("_id")
                            news_article["mongo_id"] = str(_id)
                            try:

                                    print ES_CLIENT.index(index="news", doc_type="news", body=news_article)
                            except Exception as e:
                                    print "Error --<<{0}>> in news_id=--<<{1}>>--".format(e, news_article["news_id"])
                                    pass
                
                
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
        
        #ElasticSearchSetup(renew_indexes=True)
        #PopulateElasticSearch()
        print ElasticSearchApis.do_query(text_to_search="india")












