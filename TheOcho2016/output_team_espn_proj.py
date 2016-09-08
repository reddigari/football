import numpy as np
import pandas as pd
import time, glob
import json

def output_proj_json(wk):

    json_out = []

    espn_fname = glob.glob('Data/Projections/ESPN/Wk%d/*.csv' %wk)[-1]
    roster_fname = glob.glob('TheOcho2016/Teams/Rosters*.pickled')[-1]
    espn = pd.read_csv(espn_fname)
    rosters = pd.read_pickle(roster_fname)

    proj = pd.merge(rosters, espn, on=['Player', 'Team', 'Pos'], how='inner')
    assert rosters.shape[0] == rosters.shape[0]

    # order = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'FLEX', 'Bench']
    order = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'FLEX']
    av = proj.groupby(['Slot'])['FFPts'].sum()/8.0
    av = av.reindex_axis(order, 0)
    # out = {'owner': 'AVERAGE'}
    # out['data'] = [{'Slot': pos, 'FFPts': av.ix[pos]} for pos in order]
    # json_out.append(out)

    pl = proj.groupby(['Owner', 'Slot'])['FFPts'].sum().reset_index()

    gb = pl.groupby('Owner')
    for owner in gb.groups:
        out, data_out = {}, []
        out['owner'] = owner
        d = gb.get_group(owner).set_index('Slot')
        for pos in order:
            data_out.append({'Slot': pos, 'FFPts': d.ix[pos]['FFPts']})
            out['data'] = data_out
        json_out.append(out)

    json.dump(json_out, open('TheOcho2016/weekly_performance/wk%d_proj.json' %wk, 'w'))
