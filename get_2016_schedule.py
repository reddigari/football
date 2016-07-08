import numpy as np
import pandas as pd
import requests
from football_utilities import get_team_abbr

url = 'http://www.pro-football-reference.com/years/2016/games.htm'

r = requests.get(url)
sch2016 = pd.read_html(r.text)[0]
sch2016.insert(0, 'Year', 2016)
sch2016.drop_duplicates(keep=False, inplace=True)

del sch2016['Unnamed: 4']
sch2016 = sch2016[np.invert(sch2016.Week.str.startswith('Pre'))]
sch2016.reset_index(drop=True, inplace=True)
sch2016.rename(columns={'Unnamed: 2': 'Date', 'VisTm': 'Away', 'HomeTm': 'Home'}, inplace=True)
sch2016 = sch2016.apply(pd.to_numeric, errors='ignore')

def fix_date_str(row):
    if row.Date.startswith('January') or row.Date.startswith('February'):
        return ' '.join([row.Date, str(row.Year + 1), row.Time])
    else:
        return ' '.join([row.Date, str(row.Year), row.Time])

sch2016['Date'] = sch2016.apply(fix_date_str, 1).apply(pd.to_datetime)
del sch2016['Time']
sch2016.Home = sch2016.Home.apply(lambda x: get_team_abbr(x.split()[-1]))
sch2016.Away = sch2016.Away.apply(lambda x: get_team_abbr(x.split()[-1]))

sch2016.to_csv('Data/Schedule2016.csv', index=False)
sch2016.to_pickle('Data/Schedule2016.pickled')
