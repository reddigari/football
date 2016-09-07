import numpy as np
import pandas as pd
import json
import sys

root_path = '/home/samir/Statistics/football/'
sys.path.append(root_path)

from football_utilities import get_team_abbr

## THIS IS OUT OF DATE, parse_roster DOES OTHER SHIT NOW AND THIS WILL NOT WORK
## teams should be dict output by parse_rosters

proj = pd.read_csv(root_path + 'Data/ESPN_Projections_2016.csv')
ffa_proj = pd.read_csv(root_path + 'Draft2016/FFA-CustomRankings.csv', index_col=False)

ffa_proj.team = ffa_proj.team.apply(get_team_abbr)

#fix names so they match between FFA and ESPN
ffa_proj.playername = ffa_proj.playername.str.replace("LeVeon", "Le'Veon")
ffa_proj.playername = ffa_proj.playername.str.replace("Odell Beckham", "Odell Beckham Jr.")
ffa_proj.playername = ffa_proj.playername.str.replace("Duke Johnson", "Duke Johnson Jr.")
ffa_proj.columns = ffa_proj.columns.str.replace('playername', 'Player')
ffa_proj.columns = ffa_proj.columns.str.replace('team', 'Team')

out = []
for team, roster in teams.iteritems():
    x = pd.merge(proj, roster, on=['Player', 'Team'], how='inner')
    x = pd.merge(x, ffa_proj, on=['Player', 'Team'], how='inner')
    assert(x.shape[0] == roster.shape[0])
    starters = x[x.Slot != 'Bench']
    print starters.shape[0]
    out.append({'team': team,
                'espn_pts': starters.FFPts.astype('float').sum(),
                'ffa_pts': starters.points.sum()})

json.dump(out, open('ocho_espn_projections.json', 'w'))
