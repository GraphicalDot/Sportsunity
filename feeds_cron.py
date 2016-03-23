import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import GlobalLinks
from Feeds.Cricket import BBC_Cric_Feed, CBUZ_Cric_Feed, ESPN_Cric_Feed, Ndtv_Feed, DailyMail_Cric_Feed
from Feeds.Football import Fifa_dot_com, Football_fancast, Football_uk, Goal_dot_com


def add_cricket_news():
    print 'ADD CRICKET NEWS'
    BBC_Cric_Feed.CricketBbc(GlobalLinks.CBUZ_CRIC_FEED).run()
    CBUZ_Cric_Feed.CricketCbuz(GlobalLinks.BBC_CRIC_FEED).run()
    ESPN_Cric_Feed.CricketEspn(GlobalLinks.ESPN_CRIC_FEED).run()
    Ndtv_Feed.CricketNdtv(GlobalLinks.NDTV_CRICKET_FEED).run()
    DailyMail_Cric_Feed.CricketDailyMail(GlobalLinks.MAIL_CRIC_FEED).run()


def add_football_news():
    print 'ADD FOOTBALL NEWS'
    Football_uk.FootballUk(GlobalLinks.Football_uk).run()
    Football_fancast.FootballFancast(GlobalLinks.Football_Fancast).run()
    Fifa_dot_com.FootballFifa(GlobalLinks.Fifa_dot_com).run()
    Goal_dot_com.FootballGoal(GlobalLinks.Goal_dot_com).run()



def main():
    add_cricket_news()
    add_football_news()

    # TODO:
    # add_basketball_news()
    # add_tennis_news()
    # add_f1_news()


if __name__ == "__main__":
    main()
