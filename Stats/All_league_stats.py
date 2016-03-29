#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from subprocess import call


class AllLeagues:

    def get_player_stats(self):
        print 'Bundesliga'
        call(['python','Stats/Bundesliga_Squads.py'])
        print 'Laliga'
        call(['python','Stats/Laliga_Squads.py'])
        print 'SerieA'
        call(['python','Stats/SerieA_Squads.py'])
        print 'Premier_league'
        call(['python','Stats/Premierleague_Squads'])
        print


def main():
    obj = AllLeagues()
    obj.get_player_stats()


if __name__ == "__main__":
    main()
