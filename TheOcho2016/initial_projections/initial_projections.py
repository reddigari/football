import numpy as np
import pandas as pd
import json

root_path = '/home/samir/Statistics/football/'

## teams should be dict output by parse_rosters

proj = pd.read_csv(root_path + 'Data/ESPN_Projections_2016.csv')

out = {}
for team, roster in teams.iteritems():
    x = pd.merge(proj, roster, on=['Player', 'Team'], how='inner')
    starters = x[x.Slot != 'Bench']
    print starters.shape[0]
    out[team] = starters.FFPts.astype('float').sum()


json_out = [{'team': i, 'points': j} for i, j in out.iteritems()]

json.dump(json_out, open('ocho_espn_projections.json', 'w'))
