import numpy as np
import pandas as pd
from itertools import chain

columns = np.asarray(['Year', 'Week', 'Player', 'Team', 'Pos', 'G', 'QBRat',
                      'Cmp', 'PsAtt', 'PsYds', 'PsYdsAtt', 'PsLng', 'Int',
                      'PsTD', 'RsAtt', 'RsYds', 'RsYdsAtt', 'RsLng', 'RsTD',
                      'Rec', 'Tgt', 'RcYds', 'RcYdsRec', 'RcLng', 'RcTD',
                      'Sack', 'SackYds', 'Fum', 'FumL'])

# these are the placeholder column names to drop, not indices
drop_idx = {'QB': [3, 12, 18, 21, 24],
            'RB': [3, 9, 16, 19],
            'TE': [3, 10, 16, 19],
            'WR': list(chain([3, 25], range(10,23)))}

colname_idx = {'QB': np.asarray(list(chain(range(19), range(25, 29)))),
               'RB': np.asarray(list(chain(range(6), range(14, 25), range(27, 29)))),
               'TE': np.asarray(list(chain(range(6), range(19, 25), range(14, 19), range(27, 29)))),
               'WR': np.asarray(list(chain(range(6), range(19, 25), range(27, 29))))}

data_dict = {}

for pos in ['QB', 'RB', 'TE', 'WR']:
    data = None
    for y in range(2001, 2016):
        for w in range(1, 18):
            fname = 'Data/Raw/HTML/%s_%d_Wk%d.html' %(pos, y, w)
            with open(fname, 'r') as f:
                raw = f.read()
            tables = pd.read_html(raw)
            table = tables[-1]
            table = table.drop(range(2))
            assert table.shape[0] > 20
            table.insert(0, 'Year', y)
            table.insert(1, 'Week', w)
            table.insert(4, 'Pos', pos)
            if data is None:
                data = table
            else:
                data = pd.concat([data, table])
            print pos, y, w

    data = data.drop(drop_idx[pos], axis=1)

    data.columns = columns[colname_idx[pos]]
    data = data.apply(pd.to_numeric, errors='ignore')
    data = data.reset_index(drop=True)

    data_dict[pos] = data

data = pd.concat(data_dict.values(), join='outer')
data = data.reindex_axis(columns, axis=1)
data = data.reset_index(drop=True)

missing_teams = [('Jalen Parmele', 'BAL'), ('Devin Moore', 'IND'),
                 ('Darius Reynaud', 'NYG'), ('Stefan Logan', 'DET'),
                 ('Jason Wright', 'ARI'), ('Bernard Scott', 'CIN'),
                 ('Leon Washington', 'SEA'), ('Deji Karim', 'JAC'),
                 ('Clifton Smith', 'CLE'), ('Quinn Porter', 'STL')]

for p, t in missing_teams:
    data.loc[(pd.isnull(data.Team)) & (data.Player==p), 'Team'] = t

def calc_ffpts(x):
    return np.nansum([(0.2 * np.floor(x['PsYds'] / 5)), (-2.0 * x['Int']),
                      (4.0 * x['PsTD']), (0.1 * x['RsYds']), (6.0 * x['RsTD']),
                      (0.1 * x['RcYds']), (6.0 * x['RcTD']), (-2.0 * x['FumL'])])

data['FFPts'] = data.apply(calc_ffpts, 1)

data.to_csv('Data/Offense_2001-2015.csv', index=False)
