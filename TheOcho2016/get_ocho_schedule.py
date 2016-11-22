import numpy as np
import pandas as pd
import os
from espnffl import *

latest_week = 11

lg = FFLeague('The Ocho', path=os.path.join(os.getcwd(), 'TheOcho2016'), league_id=914065)

url = 'http://games.espn.com/ffl/schedule?leagueId=914065'

raw = pd.read_html(url, attrs={'class', 'tableBody'})[0]
sch = raw.dropna(0, how='all')
idx = np.array([np.arange(i, i+4) for i in np.arange(2, 76, 6)]).flatten()
sch = sch.iloc[idx].reset_index(drop=True)
sch.drop([0,2,3], 1, inplace=True)
sch.columns = ['Away', 'Home', 'Result']
sch.insert(0, 'Week', np.repeat(np.arange(1, 14), 4))

### specific to who has a ridiculous name at time of scraping
name_map = {'Ya': u'Adam'}

def fix_names(x, owners, name_map):
    x = x.split()[0]
    if x in owners:
        return x
    else:
        return name_map[x]

sch['Away'] = sch.Away.apply(lambda x: fix_names(x, lg.owners, name_map))
sch['Home'] = sch.Home.apply(lambda x: fix_names(x, lg.owners, name_map))

def parse_score(row):
    if row['Result'] in ['Preview', 'Box']:
        return None, None, None
    scores = map(float, row['Result'].split('-'))
    teams = [row['Away'], row['Home']]
    return scores[0], scores[1], teams[np.argmax(scores)]

score_info = sch.apply(parse_score, 1)
sch['PtsAway'] = [i[0] for i in score_info]
sch['PtsHome'] = [i[1] for i in score_info]
sch['Winner'] = [i[2] for i in score_info]
del sch['Result']

sch.to_csv('TheOcho2016/TheOcho_schedule_after%d.csv' %latest_week, index=False)
