#!/usr/bin/env python
import requests
import json
import pprint

def scorecard():
        r = requests.get("https://api.litzscore.com/rest/v2/match/nzaus_2016_test_02/?access_token=2s144861828237692s707167167837259126")
	data = json.loads(r.content)
	dict2 = {}
	for t in data['data']['card']['innings'].keys():
		for player in data['data']['card']['innings'][t]['batting_order']:
			try:
				if 'dismissed' in data['data']['card']['players'][player.split('(')[0]]['match']['innings'][t.split('_')[1]]['batting'].keys():
					dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).setdefault('batting',[]).append({'player':player,
						'player_status':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['out_str'],
						'R':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['runs'],
						'B':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['balls'],
						'4s':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['fours'],
						'6s':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['sixes'],
						'SR':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['strike_rate']})
				elif data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']:
					dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).setdefault('batting',[]).append({'player':player+"*",
						'player_status':'not out',
						'R':data['data']['card']['players'][player.split('(')[0]]['match']['innings'][t.split('_')[1]]['batting']['runs'],
						'B':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['balls'],
						'4s':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['fours'],
						'6s':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['sixes'],
						'SR':data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['batting']['strike_rate']})
			except:
				pass
		for player in data['data']['card']['innings'][t]['bowling_order']:
			try:
				bowling_data = data['data']['card']['players'][player]['match']['innings'][t.split('_')[1]]['bowling']
				dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).setdefault('bowling',[]).append({'player':str(player),
					'overs':str(bowling_data['overs']),
					'economy':str(bowling_data['economy']),
					'runs':str(bowling_data['runs']),
					'wickets':str(bowling_data['wickets']),
					'extras':str(bowling_data['extras']),
					'maiden':str(bowling_data['maiden_overs'])})
			except Exception,e:
				print e

		for batsman in data['data']['card']['teams'][t.split('_')[0]]['match']['playing_xi']:
			if batsman not in data['data']['card']['innings'][t]['batting_order']:
				dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).setdefault('did_not_bat',[]).append(batsman)
			dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).update({'inning_extras':data['data']['card']['innings'][t]['extras'],
				'team_runs':data['data']['card']['innings'][t]['runs'],
				'team_wickets':data['data']['card']['innings'][t]['wickets'],
				'team_run_rate':data['data']['card']['innings'][t]['run_rate'],
				'team_overs':data['data']['card']['innings'][t]['run_str'].split('in ')[1],
				'fall_of_wickets':data['data']['card']['innings'][t]['fall_of_wickets']})
		dict2.setdefault(data['data']['card']['teams'][t.split('_')[0]]['name'],{}).setdefault(t,{}).setdefault('extras_str',[]).append({'b':str(data['data']['card']['innings'][t]['bye'])
			,'lb':str(data['data']['card']['innings'][t]['legbye']),
			'w':str(data['data']['card']['innings'][t]['wide']),
			'nb':str(data['data']['card']['innings'][t]['noball'])})
	pprint.pprint(dict2)


if __name__=='__main__':
		scorecard()
