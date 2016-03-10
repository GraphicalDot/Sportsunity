#!/usr/bin/env python

__metaclass__ = type

import sys
path = sys.path.append('Stats')
print path
import os
from subprocess import call

class AllLeagues:

        def get_player_stats(self):
                print 'Bundesliga'
                call(['python','Bundesliga_Squads.py'])
                print 'Laliga'
                call(['python','Laliga_Squads.py'])
                print 'SerieA'
                call(['python','SerieA_Squads.py'])
                print 'Premier_league'
                call(['python','Premierleague_Squads'])
                print
                

def main():
        obj = AllLeagues()
        obj.get_player_stats()



if __name__ == "__main__":main()
