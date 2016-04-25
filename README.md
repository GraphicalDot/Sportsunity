Sportsunity
The WHole development process for Sportsunity is divided into three phases

Phase 1:
	This deals with the basic infrastructure for user registrations, invites and gathering of relevant data from 
	different sources.
	Phase1.1: Feeds
		This is the Feeds module which will fetch all the news feed from different Websites for five sports.
		Right now, RSS feeds from different websites are same.

		Football Feeds:
			Fifa_dot_com = 'http://www.fifa.com/rss/index.xml'
			Football_uk = 'http://www.football.co.uk/news/rss.xml'
			Goal_dot_com = 'http://www.goal.com/en-gb/feeds/news?fmt=rss&ICID=HP'
			Football_Fancast = 'http://www.footballfancast.com/feed'

		BasketBall Feeds:
			NBA = 'http://www.nba.com/rss/nba_rss.xml'
			Real_gm = 'http://basketball.realgm.com/rss/wiretap/15/0.xml'
			Roto_world = 'http://www.rotoworld.com/rss/feed.aspx?sport=nba&ftype=article&count=12&format=rss'
			Inside_hoops = 'http://www.insidehoops.com/blog/?feed=rss2'

		Crash_dot_net = 'http://rss.feedsportal.com/c/350/f/537798/index.rss?'
			Grandprix_dot_com = 'http://grandprix.com/rss.xml'  
			Auto_sport = 'http://www.autosport.com/rss/f1news.xml'

		Tennis Feeds:
			TENNIS_DOT_COM_FEED = "http://feeds.feedburner.com/tenniscom-news"
			BBC_FEED = "http://feeds.bbci.co.uk/sport/0/tennis/rss.xml?edition=uk"
			TENNIS_X = "http://feeds.feedburner.com/tennisx?format=xml"
			CBS = "http://www.cbssports.com/partners/feeds/rss/tennis_news"

		NDTV_CRICKET_FEED = "http://feeds.feedburner.com/NDTV-Cricket"  #ndtv sportsnews feed
			ESPN_CRIC_FEED = "http://www.espncricinfo.com/rss/content/story/feeds/0.xml"
			BBC_CRIC_FEED = "http://feeds.bbci.co.uk/sport/0/cricket/rss.xml?edition=uk"
			CBUZ_CRIC_FEED = "http://live-feeds.cricbuzz.com/CricbuzzFeed" #criccbuzz sportsnews feed
			GOOG_CRIC_FEED = "https://news.google.co.in/news?pz=1&cf=all&ned=in&hl=en&topic=s&output=rss" #criccbuzz sportsnews feed
			GOOG_ALL_FEED = "https://news.google.co.in/news?cf=all&ned=country_name&hl=en&topic=s&output=rss" #criccbuzz sportsnews fe


		##TODO:
			After vesion 1.2, We will try to delete the articles which are same This will be done by
			co-refrence resolution technique of machine learning.
			
			Already prsent in elasticsearch 1.4

		Architecture:
			A Amazon VPC cluster, with the main server running the main celery worker and Mongodb hosted on EBS, 
			Celery workers will fetch tasks from redis present on this main server and will store data on the EBS.
			Only this main server will be exposed to the outer world through Apis, 
			Apis documentation can be seen at:  
					https://github.com/kaali-python/Sportsunity/wiki/FeedsApis


		Issue:
			If you think that there are some other good news websites, Please let us know.
		Status: Complete

	Phase1.2: User Registration and Profile
			This is user_registration module which deals wit the users siging in with facebook and google.
			User profile will have sections of favourite sport, players, Leagues
		
		Architecture:
			User data will be saved in Postgresql for maintaing data security with the scope of shards
			and rht now, with only one replica set, Which is extendable accoring to our needs depending
			upon the load we would entertain
		


		Issue:
			Facebook doesnt provide friendslist anymore, We can only send link to our freinds, 
			But that will notify us whenever that friend of the user will join our app.


		Status: Not Completed
		Expected: In a week

	Phase1.3:
		Player Statistics, Live Scores, Match Statistics, Upcoming sports events
		

		
Phase 2:
	Deals with group Creation, User discovery, group keywords

	Architecture:
		Chats:
			Postgresql for chat data consistency and batch storage in Elastic search.
		User Discovery:=
			Mongodb as it supports geo-location search


Phase 3:
	Deals with Match walls


#######################################################################################################################


* Installation Steps:

1. Create separate virtualenv for the repo:
>> virtualenv <env_name>
>> cd <env_name>
>> source bin/activate

2. Clone the repo:
>> git clone https://github.com/kaali-python/Sportsunity.git

3. Install the requirements
>> pip install -r requirements.py

* To start supervisor:
>> sudo supervisord -c /etc/supervisord.conf
>> sudo supervisorctl -c /etc/supervisord.conf start all
