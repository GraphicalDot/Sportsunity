#!/usr/bin/env python

import feedparser
from urllib2 import urlopen
from bs4 import BeautifulSoup
import itertools

class TennisScores:
	
	def __init__(self,url):
		self.rss = feedparser.parse(url)

	def get_scores(self):
		new_tournaments = []
		for feeds in self.rss.entries:
			new_scores = []
			new_sets = []
                        tournaments = []
			players = feeds['title'][39:].replace('#',"")
			content = urlopen(feeds['id']).read()
			soup = BeautifulSoup(content,'lxml')
			for x in soup.find_all('table',{'class':'goalpop_rd'}):
				scores = x.find_all('td',{'class':'bcen'})
				sets = x.find_all('td',{'class':'cen'})
				tournaments.append(x.find_all('td',{'class':'league'}))
			for score in scores:
				try:
					new_scores.append(score.contents[0].string.strip())
				except:
					new_scores.append(score.contents[1].string.strip())
				else:
					pass
			
			for _set in sets:
				new_sets.append(_set.string.strip())

			for val in tournaments[0]:
				new_tournaments.append(val.contents[1].string.strip())

			print players
			for tournament,_set,score1,score2 in itertools.izip(new_tournaments,new_sets,new_scores[:5],new_scores[5:]):
				print tournament+' '+_set+"--> "+score1+' - '+score2
			
			 
		

def main():
	obj = TennisScores('http://www.scorespro.com/rss2/live-tennis.xml')
	obj.get_scores()



if __name__=="__main__":
	main()	
