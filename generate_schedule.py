import pandas as pd
import requests
from football_utilities import get_team_abbr

url = 'http://www.pro-football-reference.com/years/%d/games.htm'
sch = None
for y in range(2001, 2016):
    r = requests.get(url %y)
    table = pd.read_html(r.text)[0]
    table.insert(0, 'Year', y)
    if sch is None:
        sch = table
    else:
        sch = pd.concat([sch, table])
    print "Retrieved %d schedule." %y

sch.rename(columns={'Unnamed: 4': 'At'}, inplace=True)
del sch['Unnamed: 6']

sch.columns = sch.columns.str.replace('/tie', '')
sch = sch[(sch.Winner != 'Winner/tie') & (sch.Date != 'Playoffs')]
sch.Winner = sch.Winner.apply(lambda x: get_team_abbr(x.split()[-1]))
sch.Loser = sch.Loser.apply(lambda x: get_team_abbr(x.split()[-1]))

def fix_date_str(row):
    if row.Date.startswith('January') or row.Date.startswith('February'):
        return row.Date + ' ' + str(row.Year + 1)
    else:
        return row.Date + ' ' + str(row.Year)

sch['Date'] = sch.apply(fix_date_str, 1).apply(pd.to_datetime)

homes, aways = [], []

for i, row in sch.iterrows():
    if row.At == r'@':
        home, away = row['Loser'], row['Winner']
    else:
        home, away = row['Winner'], row['Loser']
    homes.append(home)
    aways.append(away)

sch['Home'] = homes
sch['Away'] = aways
