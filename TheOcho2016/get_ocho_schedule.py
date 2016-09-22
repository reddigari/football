import numpy as pd
import pandas as pd

url = 'http://games.espn.com/ffl/schedule?leagueId=914065'

raw = pd.read_html(url, attrs={'class', 'tableBody'})[0]
sch = raw.dropna(0, how='all')
idx = np.array([np.arange(i, i+4) for i in np.arange(2, 76, 6)]).flatten()
sch = sch.iloc[idx].reset_index(drop=True)
sch.drop([0,2,3], 1, inplace=True)
sch.columns = ['Away', 'Home', 'Result']
sch.insert(0, 'Week', np.repeat(np.arange(1, 14), 4))

def parse_score(row):
    if row['Result'] == 'Preview':
        return None
    scores = map(float, row['Result'].split('-'))
    teams = [row['Away'], row['Home']]
    return teams[np.argmax(scores)]

sch['Result'] = sch.apply(parse_score, 1)
