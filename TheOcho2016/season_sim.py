import numpy as np
import pandas as pd
from collections import Counter
import copy

pp = lg.merge_proj_scores(week=latest_week, all_players=False, prev_weeks=True)
all_wk_scores = ave = pp[pp.Slot != 'Bench'].groupby(['Owner', 'Week']).sum()['FFPts_real']
stdev = all_wk_scores.std()
ave = pp[pp.Slot != 'Bench'].groupby('Owner').sum()['FFPts_real']/float(latest_week)

start_scores = Counter((7 * ave).to_dict())
start_wins = Counter(sch.Winner[sch.Winner.notnull()].values)

to_play = sch[sch.Winner.isnull()]

n_sim = 10000
sims = dict()
for team in sch.Home.unique():
    sims[team] = dict(wins=np.zeros(n_sim), pts=np.zeros(n_sim), po=np.zeros(n_sim))

def simulate_season(random=False):
    sim_scores, sim_wins = Counter(), Counter()
    for _, row in to_play.iterrows():
        if random:
            home_score, away_score = np.random.normal(96.0, 23.0, 2)
        else:
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

for i in range(10000):
    if i%500==0:
        print "Running simulation %d" %i
    wins, points = simulate_season(random=True)
    for team in wins:
        sims[team]['pts'][i] = wins[team]
        sims[team]['wins'][i] = points[team]
    po_teams = figure_playoffs(wins, points)
    for team in po_teams:
        sims[team]['po'][i] += 1
