#!/usr/bin/env python

__metaclass__ = type

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
from Feeds.Cricket.DailyMail_Cric_Feed import CricketDailyMail
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

class AllInstance:
        def __init__(self):
                #super(self).__init__()
                pass

        def basketball_instances(self):
                
                self.Instance_bask1 = BasketballNba(NBA)
                self.Instance_bask1.run()
                self.Instance_bask2 = BasketballHoops(Inside_hoops)
                self.Instance_bask2.run()
                self.Instance_bask3 = BasketballReal(Real_gm)
                self.Instance_bask3.run()
                self.Instance_bask4 = BasketballRoto(Roto_world)
                self.Instance_bask4.run()

        def cricket_instances(self):

                self.Instance_cric1 = CricketBbc(CBUZ_CRIC_FEED)
                self.Instance_cric1.run()
                self.Instance_cric2 = CricketCbuz(BBC_CRIC_FEED)
                self.Instance_cric2.run()
                self.Instance_cric3 = CricketEspn(ESPN_CRIC_FEED)
                self.Instance_cric3.run()
                self.Instance_cric4 = CricketNdtv(NDTV_CRICKET_FEED)
                self.Instance_cric4.run()
                self.Instance_cric5 = CricketDailyMail(MAIL_CRIC_FEED)
                self.Instance_cric5.run()
        
        def f1_instances(self):

                self.Instance_formula1 = FormulaAuto(Auto_sport)
                self.Instance_formula1.run()
                self.Instance_formula2 = FormulaCrash(Crash_dot_net)
                self.Instance_formula2.run()
                self.Instance_formula3 = FormulaGrand(Grandprix_dot_com)
                self.Instance_formula3.run()

        def football_instances(self):

                self.Instance_football1 = FootballUk(Football_uk)
                self.Instance_football1.run()
                self.Instance_football2 = FootballFancast(Football_Fancast)
                self.Instance_football2.run()
                self.Instance_football3 = FootballFifa(Fifa_dot_com)
                self.Instance_football3.run()
                self.Instance_football4 = FootballGoal(Goal_dot_com)
                self.Instance_football4.run()

        def tennis_instances(self):

                self.Instance_tennis1 = TennisBbc(BBC_FEED)
                self.Instance_tennis1.run()
                self.Instance_tennis2 = TennisX(TENNIS_X)
                self.Instance_tennis2.run()
                self.Instance_tennis3 = TennisWta(WTA)
                self.Instance_tennis3.run()


"""
This function fetches all the basketball
news and stores it in the database.
"""

class RunBasketball(AllInstance):
        def __init__(self):
                super(RunBasketball,self).__init__()

        def get_basknews(self):

                print "Hey there!"
                AllInstance.basketball_instances(self)


"""
This function fetches all the cricket
news and stores it in the database.
"""

class RunCricket(AllInstance):
        def __init__(self):
                super(RunCricket,self).__init__()

        def get_cricnews(self):
                
                print "Cricket"
                AllInstance.cricket_instances(self)


"""
This function fetches all the formula1
news and stores it in the database.
"""

class RunF1(AllInstance):
        def __init__(self):
                super(RunF1,self).__init__()

        def get_f1news(self):
                print "F1"
                AllInstance.f1_instances(self)


"""
This function fetches all the football
news and stores it in the database.
"""

class RunFootball(AllInstance):
        def __init__(self):
                super(RunFootball,self)
                
        def get_footnews(self):
                print "Football"
                AllInstance.football_instances(self)


"""
This function fetches all the tennis
news and stores it in the database.
"""

class RunTennis(AllInstance):
        def __init__(self):
                super(RunTennis,self)
                
        def get_tennnews(self):
                print "Tennis"
                AllInstance.tennis_instances(self)


def main():
        obj = RunBasketball()
        obj.get_basknews()

        obj1 = RunCricket()
        obj1.get_cricnews()

        obj2 = RunF1()
        obj2.get_f1news()

        obj3 = RunFootball()
        obj3.get_footnews()

        obj4 = RunTennis()
        obj4.get_tennnews()





if __name__ == "__main__":main()
