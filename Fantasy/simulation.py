s = sch[sch.PtsHome.notnull()]

s['PtsHome'] = 0.
s['PtsAway'] = 0.
s['Winner'] = np.nan

pp = lg.merge_proj_scores(week=latest_week, all_players=False, prev_weeks=True)
all_wk_scores = ave = pp[pp.Slot != 'Bench'].groupby(['Owner', 'Week']).sum()['FFPts_real']
grand_ave = all_wk_scores.mean()
stdev = all_wk_scores.std()

zero_ct = Counter()
for o in s.Home.unique():
    zero_ct[o] = 0

def simulate_season():
    sim_scores, sim_wins = Counter(), Counter()
    for _, row in s.iterrows():
        home_score, away_score = np.random.normal(grand_ave, stdev, 2)
        sim_scores[row['Home']] += home_score
        sim_scores[row['Away']] += away_score
        if home_score > away_score:
            sim_wins[row['Home']] += 1
        else:
            sim_wins[row['Away']] += 1
        sim_wins.update(zero_ct)
    return sim_wins, sim_scores

win_list, pt_list = [], []
for i in range(10000):
    w, p = simulate_season()
    win_list.append(w)
    pt_list.append(p)
    if i%1000 == 0:
        print i
