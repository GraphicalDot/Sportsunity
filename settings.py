

STATUS_200 = 200
ERROR_500 = 500
ERROR_400 = 400
ERROR_402 = 402
ERROR_404 = 404

ERROR_LIST = [ERROR_500, ERROR_400, ERROR_402, ERROR_404]

LOCAL_ELASTIC_SERVER = 'localhost'
ELASTIC_PORT = 9200

LOCAL_MONGO_HOST = 'localhost'

# old mongo servers
# MONGO_SERVERIP = 'mongodb://10.0.4.225:27017,10.0.2.249:27018, 10.0.2.117:27019/?replicaSet=fetchfeedReplicaSet'

# new mongo servers
MONGO_SERVERIP = 'mongodb://10.0.1.205:27017, 10.0.1.139:27017, 10.0.1.151:27017/?replicaSet=SportsNewsReplicaSet'

# MONGO_SERVERIP = 'mongodb://localhost:27017'
# MONGO_PORT = 27017

#SCORES server config
SCORES_SERVERIP = '52.74.75.79'
SCORES_SERVER_PORT = 8000

SCORES_SERVERIP = 'localhost'
SCORES_SERVER_PORT = 8000

# teams_elasicsearch.py settings
FOOTBALL_LEAGUE_IDS = ['1269','1399','1229','1221','1204']
GET_LEAGUE_STANDINGS_URL = 'http://{}:{}/get_league_standings?league_id={}'
