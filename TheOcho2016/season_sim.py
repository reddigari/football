import numpy as np
import pandas as pd
from collections import Counter
import copy, os, glob, json
from espnffl import *

latest_week = 8

sch = pd.read_csv('TheOcho2016/TheOcho_schedule_after%d.csv' %latest_week)
lg = FFLeague('The Ocho', path=os.path.join(os.getcwd(), 'TheOcho2016'), league_id=914065)

pp = lg.merge_proj_scores(week=latest_week, all_players=False, prev_weeks=True)
all_wk_scores = ave = pp[pp.Slot != 'Bench'].groupby(['Owner', 'Week']).sum()['FFPts_real']
grand_ave = all_wk_scores.mean()
stdev = all_wk_scores.std()
ave = pp[pp.Slot != 'Bench'].groupby('Owner').sum()['FFPts_real']/float(latest_week)

start_scores = Counter((latest_week * ave).to_dict())
start_wins = Counter(sch.Winner[sch.Winner.notnull()].values)

to_play = sch[sch.Winner.isnull()]

def simulate_season(assumption="random"):
    sim_scores, sim_wins = Counter(), Counter()
    for _, row in to_play.iterrows():
        if assumption=="random":
            home_score, away_score = np.random.normal(grand_ave, stdev, 2)
        elif assumption=="trend":
            home_score= np.random.normal(np.mean([grand_ave, ave[row['Home']]]), stdev)
            away_score= np.random.normal(np.mean([grand_ave, ave[row['Away']]]), stdev)
        elif assumption=="team_average":
            home_score = np.random.normal(ave[row['Home']], stdev)
            away_score = np.random.normal(ave[row['Away']], stdev)
        sim_scores[row['Home']] += home_score
        sim_scores[row['Away']] += away_score
        if home_score > away_score:
            sim_wins[row['Home']] += 1
        else:
            sim_wins[row['Away']] += 1
    sim_scores.update(start_scores)
    sim_wins.update(start_wins)
    return sim_wins, sim_scores

def figure_playoffs(ws, pts):
    teams_in = []
    while len(teams_in) < 4:
        max_pts = max(ws.values())
        top = [t for t, w in ws.items() if w == max_pts]
        if len(top) == 1:
            winner = top[0]
        else:
            pt_tots = [pts[t] for t in top]
            max_idx = np.argmax(pt_tots)
            winner = top[max_idx]
        teams_in.append(winner)
        del ws[winner]
    return teams_in

n_sim = 10000
all_sims = dict()

for assumption in ['team_average', 'trend', 'random']:
    sims = dict()
    for team in sch.Home.unique():
        sims[team] = dict(wins=np.zeros(n_sim), pts=np.zeros(n_sim), poChance=np.zeros(n_sim))

    for i in range(n_sim):
        if i % 1000 == 0:
            print "Running simulation %d" %i
        wins, points = simulate_season(assumption=assumption)
        for team in wins:
            sims[team]['wins'][i] = wins[team]
            sims[team]['pts'][i] = points[team]
        po_teams = figure_playoffs(wins, points)
        for team in po_teams:
            sims[team]['poChance'][i] += 1

    all_sims[assumption] = sims

# get records
info_fname = sorted(glob.glob(os.path.join(lg.path, 'Teams', 'TeamInfo*Wk%d*.csv' %(latest_week+1))))[0]
info = pd.read_csv(info_fname).set_index('Owner')
info['record'] = info.apply(lambda r: '%d-%d' %(r['W'], r['L']), 1)

# output json for visualization
out = dict()
for sim in all_sims:
    out[sim] = []
    for t, data in all_sims[sim].items():
        summary = dict()
        summary['team'] = t
        summary['record'] = info.ix[t]['record']
        summary['pts'] = dict(mean=data['pts'].mean(), pct10=np.percentile(data['pts'], 10), pct90=np.percentile(data['pts'], 90))
        summary['poChance'] = data['poChance'].mean()
        c = Counter(data['wins'])
        summary['wins'] = dict(mean=data['wins'].mean(), dist=[{'w': w, 'freq': ct/10000.} for w, ct in c.items()])
        out[sim].append(summary)

with open('TheOcho2016/sim_data.json', 'w') as f:
    json.dump(out, f)
