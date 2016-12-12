import numpy as np
import pandas as pd
from collections import Counter
import copy, os, glob, json
from espnffl import *

latest_week = 11

sch = pd.read_csv('Fantasy/generic_schedule.csv')

teams = sch.Home.unique()
s0 = Counter(dict.fromkeys(teams, 0))
w0 = Counter(dict.fromkeys(teams, 0))

grand_ave = 94.70
stdev = 21.12

def simulate_season():
    sim_scores, sim_wins = Counter(), Counter()
    for _, row in sch.iterrows():
        home_score, away_score = np.random.normal(grand_ave, stdev, 2)

        sim_scores[row['Home']] += home_score
        sim_scores[row['Away']] += away_score
        if home_score > away_score:
            sim_wins[row['Home']] += 1
        else:
            sim_wins[row['Away']] += 1
    sim_scores.update(s0)
    sim_wins.update(s0)
    return sim_wins, sim_scores

## needs to account for stupid conference rule
## top team from both each conference makes playoffs, then two highest records
conferences = {'East': ['Team%d' %i for i in range(1,5)],
               'West': ['Team%d' %i for i in range(4,9)]}

def find_top_team(ws, pts):
    max_ws = max(ws.values())
    top = [t for t, w in ws.items() if w == max_ws]
    if len(top) == 1:
        return top[0]
    else:
        pt_tots = [pts[t] for t in top]
        max_idx = np.argmax(pt_tots)
        return top[max_idx]

def figure_playoffs(ws, pts, conf_dict):
    teams_in = []
    for conf, teams in conf_dict.items():
        conf_ws = {t: ws[t] for t in teams}
        winner = find_top_team(conf_ws, pts)
        teams_in.append(winner)
        del ws[winner]
    for i in range(2):
        winner = find_top_team(ws, pts)
        teams_in.append(winner)
        del ws[winner]
    return teams_in


n_sim = 10000

sims = dict()
for team in teams:
    sims[team] = dict(wins=np.zeros(n_sim), pts=np.zeros(n_sim), poChance=np.zeros(n_sim))

for i in range(n_sim):
    if i % 1000 == 0:
        print "Running simulation %d" %i
    wins, points = simulate_season()
    for team in wins:
        sims[team]['wins'][i] = wins[team]
        sims[team]['pts'][i] = points[team]
    po_teams = figure_playoffs(wins, points, conferences)
    for team in po_teams:
        sims[team]['poChance'][i] += 1

# output json for visualization
# out = dict()
# for sim in all_sims:
#     out[sim] = []
#     for t, data in all_sims[sim].items():
#         summary = dict()
#         summary['team'] = t
#         summary['record'] = info.ix[t]['record']
#         summary['pts'] = dict(mean=data['pts'].mean(), pct10=np.percentile(data['pts'], 10), pct90=np.percentile(data['pts'], 90))
#         summary['poChance'] = data['poChance'].mean()
#         c = Counter(data['wins'])
#         summary['wins'] = dict(mean=data['wins'].mean(), dist=[{'w': w, 'freq': ct/10000.} for w, ct in c.items()])
#         out[sim].append(summary)
#
# with open('TheOcho2016/Visualizations/sim_data.json', 'w') as f:
#     json.dump(out, f)
