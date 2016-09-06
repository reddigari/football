import numpy as np
import pandas as pd
import time
import sys

util_path = '/home/samir/Statisitcs/football'
sys.path.append(util_path)

from football_utilities import split_espn_plr

url = 'http://games.espn.com/ffl/leaguerosters?leagueId=914065'

d = pd.read_html(url, attrs={'class': 'playerTableTable tableBody'})

teams = {}

for team in d:
    t = team.iloc[0,0].split(' (')[0]
    team.drop(range(2), inplace=True)
    team.columns = ['Slot', 'Player', 'Acq']
    team.Player = team.Player.astype('unicode')
    team.dropna(0, inplace=True)
    team.insert(2, 'Team', team.Player.apply(lambda x: split_espn_plr(x, 'team')))
    team.insert(2, 'Pos', team.Player.apply(lambda x: split_espn_plr(x, 'pos')))
    team['Player'] = team.Player.apply(lambda x: split_espn_plr(x, 'name'))
    teams[t] = team
