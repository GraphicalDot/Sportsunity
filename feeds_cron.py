import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import GlobalLinks
from Feeds.Cricket import BBC_Cric_Feed, CBUZ_Cric_Feed, ESPN_Cric_Feed, Ndtv_Feed, DailyMail_Cric_Feed
from Feeds.Football import Fifa_dot_com, Football_fancast, Football_uk, Goal_dot_com
from Feeds.basketball import Inside_hoops_Feed, NBA_Feed, Real_gm_Feed, Roto_world_Feed
from Feeds.Tennis import BBC_Feed, Tennis_X_Feed, WTA_Feed
from Feeds.F1 import Auto_sport_Feed, Crash_Feed, Grandprix_Feed


def add_cricket_news():
    """
    This function fetches all the cricket
    news and stores it in the database.
    """
    print 'ADD CRICKET NEWS'
    BBC_Cric_Feed.CricketBbc(GlobalLinks.CBUZ_CRIC_FEED).run()
    CBUZ_Cric_Feed.CricketCbuz(GlobalLinks.BBC_CRIC_FEED).run()
    ESPN_Cric_Feed.CricketEspn(GlobalLinks.ESPN_CRIC_FEED).run()
    Ndtv_Feed.CricketNdtv(GlobalLinks.NDTV_CRICKET_FEED).run()
    DailyMail_Cric_Feed.CricketDailyMail(GlobalLinks.MAIL_CRIC_FEED).run()


def add_football_news():
    """
    This function fetches all the football
    news and stores it in the database.
    """
    print 'ADD FOOTBALL NEWS'
    Football_uk.FootballUk(GlobalLinks.Football_uk).run()
    Football_fancast.FootballFancast(GlobalLinks.Football_Fancast).run()
    Fifa_dot_com.FootballFifa(GlobalLinks.Fifa_dot_com).run()
    Goal_dot_com.FootballGoal(GlobalLinks.Goal_dot_com).run()


def add_basketball_news():
    """
    This function fetches all the basketball
    news and stores it in the database.
    """
    print 'ADD BASKETBALL NEWS'
    NBA_Feed.BasketballNba(GlobalLinks.NBA).run()
    Inside_hoops_Feed.BasketballHoops(GlobalLinks.Inside_hoops).run()
    Real_gm_Feed.BasketballReal(GlobalLinks.Real_gm).run()
    Roto_world_Feed.BasketballRoto(GlobalLinks.Roto_world).run()


def add_tennis_news():
    """
    This function fetches all the tennis
    news and stores it in the database.
    """
    print 'ADD TENNIS NEWS'
    BBC_Feed.TennisBbc(GlobalLinks.BBC_FEED).run()
    Tennis_X_Feed.TennisX(GlobalLinks.TENNIS_X).run()
    WTA_Feed.TennisWta(GlobalLinks.WTA).run()


def add_f1_news():
    """
    This function fetches all the formula1
    news and stores it in the database.
    """
    print 'ADD F1 NEWS'
    Auto_sport_Feed.FormulaAuto(GlobalLinks.Auto_sport).run()
    Crash_Feed.FormulaCrash(GlobalLinks.Crash_dot_net).run()
    Grandprix_Feed.FormulaGrand(GlobalLinks.Grandprix_dot_com).run()


def main():
    add_cricket_news()
    add_football_news()
    # add_basketball_news()
    # add_tennis_news()
    # add_f1_news()


if __name__ == "__main__":
    main()
