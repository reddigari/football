import numpy as np
import pandas as pd
import sys, requests, time

root_path = '/home/samir/Statistics/football/'
sys.path.append(root_path)

from football_utilities import split_espn_plr

url_str = 'http://games.espn.com/ffl/tools/projections?&slotCategoryId=%d&startIndex=%d'
columns = ['Rk', 'Player', 'Cmp_Att', 'PsYds', 'PsTD', 'Int', 'RsAtt', 'RsYds', 'RsTD', 'Rec', 'RcYds', 'RcTD', 'FFPts']

proj = pd.DataFrame()
keep_going = True

for id, pos in zip([0, 2, 4, 6, 16, 17], ['QB', 'RB', 'WR', 'TE', 'DST', 'K']):
    idx = 0
    while True:
        url = url_str %(id, idx)
        print idx
        r = requests.get(url)
        d = pd.read_html(r.content, attrs={'id': 'playertable_0'})
        assert len(d) == 1
        d = d[0]
        if d.shape[0] == 1:
            break
        d.drop(range(2), inplace=True)
        d.columns = columns
        d.insert(2, 'Pos', pos)
        proj = pd.concat([proj, d])
        idx += 40

info = proj.Player.apply(split_espn_plr)
proj['Player'] = [i[0] for i in info]
proj.insert(2, 'Team', [i[1] for i in info])

proj.reset_index(drop=True, inplace=True)

proj.to_csv(root_path + 'Data/ESPN_Projections_2016_%s.csv' %time.strftime('%Y%d%m'), index=False)
