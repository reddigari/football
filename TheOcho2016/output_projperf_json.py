import numpy as np
import pandas as pd
import time, glob
import json

def output_projperf_json(wk):

    json_out = []

    proj_fname = glob.glob('TheOcho2016/Projections/Wk%d/ESPN*.csv' %wk)[-1]
    score_fname = glob.glob('TheOcho2016/Scores/Wk%d/ESPN*.csv' %wk)[-1]
    roster_fname = glob.glob('TheOcho2016/Teams/Rosters*.pickled')[-1]
    proj = pd.read_csv(proj_fname)
    score = pd.read_csv(score_fname)
    rosters = pd.read_pickle(roster_fname)

    proj = pd.merge(rosters, proj, on=['Player', 'Team', 'Pos'], how='inner')
    assert proj.shape[0] == rosters.shape[0]

    pp = pd.merge(proj, score, on=['Player', 'Team', 'Pos'], how='inner', suffixes=['_proj', '_real'])
    assert pp.shape[0] == rosters.shape[0]

    # order = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'FLEX', 'Bench']
    order = ['QB', 'RB', 'WR', 'TE', 'K', 'D/ST', 'FLEX']
    # av = proj.groupby(['Slot'])['FFPts'].sum()/8.0
    # av = av.reindex_axis(order, 0)
    # out = {'owner': 'AVERAGE'}
    # out['data'] = [{'Slot': pos, 'FFPts': av.ix[pos]} for pos in order]
    # json_out.append(out)

    pl = pp.groupby(['Owner', 'Slot']).agg({'FFPts_proj': np.sum,
                                            'FFPts_real': np.sum,
                                            'Player': lambda x: ' & '.join(x)})
    pl.reset_index(inplace=True)
    pl.fillna(0, inplace=True)

    gb = pl.groupby('Owner')
    for owner in gb.groups:
        out, data_out = {}, []
        out['owner'] = owner
        d = gb.get_group(owner).set_index('Slot')
        for pos in order:
            data_out.append({'Slot': pos,
                             'proj': d.ix[pos]['FFPts_proj'],
                             'pts': d.ix[pos]['FFPts_real'],
                             'player': d.ix[pos]['Player']})
            out['data'] = data_out
        json_out.append(out)
        
    json.dump(json_out, open('TheOcho2016/weekly_performance/wk%d.json' %wk, 'w'))

    return pp
