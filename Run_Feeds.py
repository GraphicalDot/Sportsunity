#!/usr/bin/env python


import sys
import os
parent_dir_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print parent_dir_path
sys.path.append(parent_dir_path)
from Feeds.basketball.Inside_hoops_Feed import BasketballHoops
from Feeds.basketball.NBA_Feed import BasketballNba
from Feeds.basketball.Real_gm_Feed import BasketballReal
from Feeds.basketball.Roto_world_Feed import BasketballRoto
from Feeds.Cricket.BBC_Cric_Feed import CricketBbc
from Feeds.Cricket.CBUZ_Cric_Feed import CricketCbuz
from Feeds.Cricket.ESPN_Cric_Feed import CricketEspn
from Feeds.Cricket.Ndtv_Feed import CricketNdtv
from Feeds.F1.Auto_sport_Feed import FormulaAuto
from Feeds.F1.Crash_Feed import FormulaCrash
from Feeds.F1.Grandprix_Feed import FormulaGrand
from Feeds.Football.Fifa_dot_com import FootballFifa
from Feeds.Football.Football_fancast import FootballFancast
from Feeds.Football.Football_uk import FootballUk
from Feeds.Football.Goal_dot_com import FootballGoal
from Feeds.Tennis.BBC_Feed import TennisBbc
from Feeds.Tennis.Tennis_X_Feed import TennisX
from Feeds.Tennis.WTA_Feed import TennisWta
from GlobalLinks import *


Instance_bask1 = BasketballNba(NBA)
Instance_bask2 = BasketballHoops(Inside_hoops)
Instance_bask3 = BasketballReal(Real_gm)
Instance_bask4 = BasketballRoto(Roto_world)

Instance_cric1 = CricketBbc(CBUZ_CRIC_FEED)
Instance_cric2 = CricketCbuz(BBC_CRIC_FEED)
Instance_cric3 = CricketEspn(ESPN_CRIC_FEED)
Instance_cric4 = CricketNdtv(NDTV_CRICKET_FEED)

Instance_formula1 = FormulaAuto(Auto_sport)
Instance_formula2 = FormulaCrash(Crash_dot_net)
Instance_formula3 = FormulaGrand(Grandprix_dot_com)

Instance_football1 = FootballUk(Football_uk)
Instance_football2 = FootballFancast(Football_Fancast)
Instance_football3 = FootballFifa(Fifa_dot_com)
Instance_football4 = FootballGoal(Goal_dot_com)

Instance_tennis1 = TennisBbc(BBC_FEED)
Instance_tennis2 = TennisX(TENNIS_X)
Instance_tennis3 = TennisWta(WTA)


class GetNewsFeeds():
        
        """
        This function fetches all the basketball
        news and stores it in the database.
        """
        def run_basketball_rss(self):
                print "Inside basketball_rss"
                Instance_bask1.run()
                Instance_bask2.run()
                Instance_bask3.run()
                Instance_bask4.run()

        """
        This function fetches all the cricket
        news and stores it in the database.
        """
        
        def run_cricket_rss(self):
                print "Inside cricket_rss"
                Instance_cric1.run()
                Instance_cric2.run()
                Instance_cric3.run()
                Instance_cric4.run()

        """
        This function fetches all the formula1
        news and stores it in the database.
        """

        def run_f1_rss(self):
                print "Inside F1_rss"
                Instance_formula1.run()
                Instance_formula2.run()
                Instance_formula3.run()

        """
        This function fetches all the football
        news and stores it in the database.
        """

        def run_football_rss(self):
                print "Inside Football_rss"
                Instance_football1.run()
                Instance_football2.run()
                Instance_football3.run()
                Instance_football4.run()

        """
        This function fetches all the tennis
        news and stores it in the database.
        """

        def run_tennis_rss(self):
                print "Inside Tennis_rss"
                Instance_tennis1.run()
                Instance_tennis2.run()
                Instance_tennis3.run()


if __name__ == "__main__":
        obj = GetNewsFeeds()
        obj.run_basketball_rss()
        obj.run_cricket_rss()
        obj.run_f1_rss()
        obj.run_football_rss()
        obj.run_tennis_rss()
