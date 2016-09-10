import numpy as np
import pandas as pd
import sys, re, time

util_path = '/home/samir/Statisitcs/football'
sys.path.append(util_path)

from football_utilities import split_espn_plr

url = 'http://games.espn.com/ffl/leaguerosters?leagueId=914065'

d = pd.read_html(url, attrs={'class': 'playerTableTable tableBody'})

owners = ['MATT', 'DANIEL', 'SAMIR', 'TYLER', 'DAVID', 'ADAM', 'SCOTT', 'PETR']

rosters = pd.DataFrame()
teams = []
r = re.compile('(.*?) \((\d)-(\d)\)')

for n, roster in enumerate(d):
    m = r.match(roster.iloc[0,0])
    roster.drop(range(2), inplace=True)
    roster.columns = ['Slot', 'Player', 'Acq']
    roster.Player = roster.Player.astype('unicode')
    roster.dropna(0, inplace=True)
    info = roster.Player.apply(split_espn_plr)
    roster['Player'] = [i[0] for i in info]
    roster.insert(2, 'Team', [i[1] for i in info])
    roster.insert(2, 'Pos', [i[2] for i in info])
    roster['Owner'] = owners[n]
    rosters = pd.concat([rosters, roster])
    teams.append({'Owner': owners[n], 'Team': m.group(1), 'W': int(m.group(2)), 'L': int(m.group(3))})

rosters.reset_index(drop=True, inplace=True)
teams = pd.DataFrame.from_records(teams)
teams = teams.reindex_axis(['Owner', 'Team', 'W', 'L'], axis=1)

rosters.to_pickle('TheOcho2016/Teams/Rosters_%s.pickled' %time.strftime('%Y%m%d'))
teams.to_pickle('TheOcho2016/Teams/TeamInfo_%s.pickled' %time.strftime('%Y%m%d'))
