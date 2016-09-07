import numpy as np
import pandas as pd
from football_utilites import get_team_abbr


## DO NOT USE THIS, THE SITE IS MISSING DATA FOR SOME WEEKS

pos = 'DEF'
data = pd.DataFrame()
for y in range(2006, 2016):
    for w in range(1, 18):
        fname = 'Data/Raw/HTML/%s_%d_Wk%d.html' %(pos, y, w)
        with open(fname, 'r') as f:
            raw = f.read()
        tables = pd.read_html(raw)
        table = tables[-1]
        table = table.iloc[:, :-3]
        table.insert(0, 'Year', y)
        table.insert(1, 'Week', w)
        table.insert(4, 'Pos', pos)
        data = pd.concat([data, table])
        print "Parsing HTML for %ss, Week %d, %d" %(pos, w, y)

columns = ['Year', 'Week', 'City', 'Team', 'Pos', 'FFPts', 'Sack', 'FR', 'Int', 'TD', 'Sfty', 'RsYdsA', 'PsYdsA', 'TotYdsA']
data.columns = columns
data.Team = data.Team.apply(get_team_abbr)
del data['City']
