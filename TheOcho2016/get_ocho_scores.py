import numpy as np
import pandas as pd
import sys, requests, time

root_path = '/home/samir/Statistics/football/'
sys.path.append(root_path)

from football_utilities import split_espn_plr

def get_ocho_scores(wk):
    url_str = 'http://games.espn.com/ffl/leaders?&scoringPeriodId=%d&seasonId=2016&slotCategoryId=%d&startIndex=%d&leagueId=914065'
    columns = ['Player', 'OwnCode', 'Action', 'Opp', 'WLScore', 'Cmp_Att', 'PsYds', 'PsTD', 'Int', 'RsAtt', 'RsYds', 'RsTD', 'Rec', 'RcYds', 'RcTD', 'Tgt', '2PC', 'FumL', 'MiscTD', 'FFPts']

    scores = pd.DataFrame()
    keep_going = True

    for id, pos in zip([0, 2, 4, 6, 16, 17], ['QB', 'RB', 'WR', 'TE', 'DST', 'K']):
        idx = 0
        while True:
            url = url_str %(wk, id, idx)
            print pos, idx
            r = requests.get(url)
            d = pd.read_html(r.content, attrs={'id': 'playertable_0'})
            assert len(d) == 1
            d = d[0]
            if d.shape[0] == 1:
                break
            d.drop(range(2), inplace=True)
            d.drop([1,4,7,12,16,21,25], axis=1, inplace=True)
            d.columns = columns
            d.insert(2, 'Pos', pos)
            scores = pd.concat([scores, d])
            idx += 50 #scoring leaders show 50 per page, vs 40 for projections

    info = scores.Player.apply(split_espn_plr)
    scores['Player'] = [i[0] for i in info]
    scores.insert(2, 'Team', [i[1] for i in info])
    scores = scores.replace('--', np.nan)
    scores = scores.apply(pd.to_numeric, errors='ignore')

    scores.reset_index(drop=True, inplace=True)

    scores.to_csv('TheOcho2016/Scores/Wk%d/ESPN_Scores_2016Wk%d_%s.csv' %(wk, wk, time.strftime('%Y%m%d')), index=False)

    return scores
