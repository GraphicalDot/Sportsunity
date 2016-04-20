

STATUS_200 = 200
ERROR_500 = 500
ERROR_400 = 400
ERROR_402 = 402
ERROR_404 = 404

ERROR_LIST = [ERROR_500, ERROR_400, ERROR_402, ERROR_404]

ELASTIC_SERVER = 'http://10.0.1.253'
ELASTIC_PORT = 9200

# new mongo servers
MONGO_SERVERIP = 'mongodb://10.0.1.205:27017, 10.0.1.139:27017, 10.0.1.151:27017/?replicaSet=SportsNewsReplicaSet'
MONGO_PORT = 27017

#SCORES server config
SCORES_SERVERIP = 'ScoresLB-822670678.ap-northeast-2.elb.amazonaws.com'
SCORES_SERVER_PORT = 80

# teams_elasicsearch.py settings
FOOTBALL_LEAGUE_IDS = ['1269','1399','1229','1221','1204']
GET_LEAGUE_STANDINGS_URL = 'http://{}:{}/get_league_standings?league_id={}'
