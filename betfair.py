#!/usr/bin/env python


import requests
import pprint
import json
import datetime

class BetfairOdds:
    
    def __init__(self):
        self.endpoint = "https://api-au.betfair.com/exchange/betting/rest/v1/"
        self.endpoint_uk = "https://api.betfair.com/exchange/betting/rest/v1/"
        self.headers = {'X-Application': 'Y0yB2Zob0L0dSONJ', 'X-Authentication': '00yj1cCIAC0t+53kc0ODiPTpWIpTejlH4y99UYd+o80=', 'content-type': 'application/json'}
        self.list_of_competitions = []
        self.list_of_market = []
        self.dict1 = {}


    def get_marketID(self):
        now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        url = self.endpoint_uk + "listEvents/"
        json_req = '{"filter":{ "eventTypeIds":["4"] }, "max_results":"30"}'
        response = requests.post(url,data=json_req,headers=self.headers)
        self.list_of_competitions = json.loads(response.content)
        print self.list_of_competitions
        url = self.endpoint + "listEvents/"
        response = requests.post(url,data=json_req,headers=self.headers)
        for x in json.loads(response.content):
            self.list_of_competitions.append(x)
        for comp in self.list_of_competitions:
            if self.list_of_competitions.count(comp)>1:
                self.list_of_competitions.remove(comp)
        for competition in self.list_of_competitions:
            eventId = competition['event']['id']
            market_catalouge_req = '{"filter":{"eventIds":["' + eventId + '"],"marketTypeCodes":["MATCH_ODDS"],"marketBettingTypes":["ODDS"],"marketStartTime":{"from":"' + now + '"}},"sort":"FIRST_TO_START",\
                    "maxResults":"100","marketProjection":["RUNNER_METADATA","RUNNER_DESCRIPTION","COMPETITION","MARKET_START_TIME"]}'
            url = self.endpoint_uk + "listMarketCatalogue/"
            response = requests.post(url,data=market_catalouge_req,headers=self.headers)
            if json.loads(response.content):
                self.list_of_market.append(json.loads(response.content)[0])
            elif not json.loads(response.content):
                url = self.endpoint + "listMarketCatalogue/"
                response = requests.post(url,data=market_catalouge_req,headers=self.headers)
                if json.loads(response.content):
                    self.list_of_market.append(json.loads(response.content)[0])
            else:
                print competition

        pprint.pprint(self.list_of_market)

        res = requests.get('http://52.74.142.219:8000/get_all_matches_list')
        list_of_recent_cricket_matches = json.loads(res.content)

        for x in self.list_of_market:
            for match in list_of_recent_cricket_matches['data']['cricket']:
                if match['team_1'] in [x['runners'][0]['runnerName']]+[x['runners'][1]['runnerName']] and match['team_2'] in [x['runners'][0]['runnerName']]+[x['runners'][1]['runnerName']]:
                    runners = x['runners']
                    for runner in runners:
                        self.get_book(x['competition']['id'],x['competition']['name'],x['marketId'],runner['runnerName'],runner['selectionId'])

        print
        pprint.pprint(self.dict1)

    def get_book(self,competitionId,competitionName,marketId,runnerName,selectionId):
        market_book_req = '{"marketIds":["' + marketId + '"],"priceProjection":{"priceData":["EX_BEST_OFFERS"]}}'
        url = self.endpoint + "listMarketBook/"
        response = requests.post(url,data=market_book_req,headers=self.headers)
        if json.loads(response.content):
            marketBook = json.loads(response.content)
            try:
                runners = marketBook[0]['runners']
                for runner in runners:
                    if runner['selectionId']==selectionId:
                        print 'Odds of '+ str(runnerName) +' winning : ' + str(runner['ex']['availableToBack'][1]['price'])
                        self.dict1.setdefault(marketId,{}).setdefault(competitionName,[]).append({runnerName:str(runner['ex']['availableToBack'][1]['price'])})
                        print competitionName,competitionId,runnerName
                        #pprint.pprint(self.dict1)
                        print
                    else:
                        print 'didn\'t match'
            except Exception,e:
                print e

        elif not json.loads(response.content):
            url = self.endpoint_uk + "listMarketBook/"
            response = requests.post(url,data=market_book_req,headers=self.headers)
            marketBook = json.loads(response.content)
            try:
                runners = marketBook[0]['runners']
                for runner in runners:
                    if runner['selectionId']==selectionId:
                        print 'Odds of ' + str(runnerName) +' winning : ' + str(runner['ex']['availableToBack'][1]['price'])
                        self.dict1.setdefault(marketId,{}).setdefault(competitionName,[]).append({runnerName:str(runner['ex']['availableToBack'][1]['price'])})
                        print competitionName,competitionId,runnerName
                        #pprint.pprint(self.dict1)
                        print
                    else:
                        print 'didn\'t match'
            except Exception,e:
                print e

        #pprint.pprint(self.dict1)


def main():
    obj = BetfairOdds()
    obj.get_marketID()


if __name__ == "__main__":main()


