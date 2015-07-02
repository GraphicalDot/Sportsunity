#!/usr/bin/env python


import sys
from Feeds.basketball.NBA_Feed import Basketball_NBA
from Feeds.basketball.Inside_hoops_Feed import Basketball_Hoops
from Feeds.basketball.Real_gm_Feed import Basketball_Real
from Feeds.basketball.Roto_world_Feed import Basketball_Roto
from Feeds.Cricket.BBC_Cric_Feed import Cricket_BBC
from Feeds.Cricket.CBUZ_Cric_Feed import Cricket_CBUZ
from Feeds.Cricket.ESPN_Cric_Feed import Cricket_ESPN
from Feeds.Cricket.Ndtv_Feed import Cricket_NDTV
from Feeds.F1.Auto_sport_Feed import Formula_one_Auto
from Feeds.F1.Crash_Feed import Formula_one_Crash
from Feeds.F1.Grandprix_Feed import Formula_one_Grandprix
from Feeds.Football.Fifa_dot_com import Football_Fifa
from Feeds.Football.Football_fancast import Football_Fancast
from Feeds.Football.Football_uk import Football_UK
from Feeds.Football.Goal_dot_com import Football_Goal
from Feeds.Tennis.BBC_Feed import Tennis_BBC
from Feeds.Tennis.Tennis_X_Feed import Tennis_X
from Feeds.Tennis.WTA_Feed import Tennis_WTA

Instance_bask1 = Basketball_NBA()
Instance_bask2 = Basketball_Hoops()
Instance_bask3 = Basketball_Real()
Instance_bask4 = Basketball_Roto()

Instance_cric1 = Cricket_BBC()
Instance_cric2 = Cricket_CBUZ()
Instance_cric3 = Cricket_ESPN()
Instance_cric4 = Cricket_NDTV()

Instance_formula1 = Formula_one_Auto()
Instance_formula2 = Formula_one_Crash()
Instance_formula3 = Formula_one_Grandprix()

Instance_football1 = Football_Fifa()
Instance_football2 = Football_fancast()
Instance_football3 = Football_UK()
Instance_football4 = Football_Goal()

Instance_tennis1 = Tennis_BBC()
Instance_tennis2 = Tennis_X()
Instance_tennis3 = Tennis_WTA()

"""
This function fetches all the basketball
news and stores it in the database.
"""

def run_basketball_rss():
    Instance_bask1.run()
    Instance_bask2.run()
    Instance_bask3.run()
    Instance_bask4.run()

def run_cricket_rss():
    Instance_cric1.run()
    Instance_cric2.run()
    Instance_cric3.run()
    Instance_cric4.run()

def run_f1_rss():
    Instance_formula1.run()
    Instance_formula2.run()
    Instance_formula3.run()

def run_football_rss():
    Instance_football1.run()
    Instance_football2.run()
    Instance_football3.run()
    Instance_football4.run()

def run_tennis_rss():
    Instance_tennis1.run()
    Instance_tennis2.run()
    Instance_tennis3.run()


if __name__ == "__main__":
    run_basketball_rss()
    run_f1_rss
