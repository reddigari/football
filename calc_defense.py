import pandas as pd
import numpy as np

## Takes offense data and calculates defensive allowances of opponent by week (sums offense)
## Calculates season-to-date averages and merges with defense data to show season performance vs actual performance
## Calculates various ranks as well as fantasy points specific to passing, receiving, and rushing

#data should be all offense

defense = data.groupby(['Year', 'Opp', 'Week']).sum().reset_index()
defense['PsFFPts'] = defense.apply(lambda x: np.nansum([(0.2 * np.floor(x['PsYds'] / 5)), (-2.0 * x['Int']), (4.0 * x['PsTD'])]), 1)
defense['RsFFPts'] = defense.apply(lambda x: np.nansum([(0.1 * x['RsYds']), (6.0 * x['RsTD'])]), 1)
defense['RcFFPts'] = defense.apply(lambda x: np.nansum([(0.1 * x['RcYds']), (6.0 * x['RcTD'])]), 1)
defense.columns = defense.columns.str.replace('Opp', 'Team')
defense.columns = defense.columns.str.replace('FumL', 'FumR')

keep = ['Year', 'Team', 'Week', 'Cmp', 'PsAtt', 'PsYds', 'Int', 'PsTD', 'RsAtt', 'RsYds', 'RsTD', 'Sack', 'SackYds', 'Fum', 'FumR', 'FFPts', 'PsFFPts', 'RsFFPts', 'RcFFPts']
defense = defense[keep]

pred = pd.DataFrame()

for y in range(2001, 2016):
    for w in range(2, 18):
        tmp = defense[(defense.Year==y) & (defense.Week<w)]
        tmwk = tmp.groupby('Team').mean()
        tmwk['Week'] = w
        tmwk['PsRnk'] = np.argsort(tmwk.PsYds)+1
        tmwk['RsRnk'] = np.argsort(tmwk.RsYds)+1
        for cat in ['Ps', 'Rs', 'Rc']:
            tmwk['%sFFPtsRk' %cat] = np.argsort(tmwk['%sFFPts' %cat])
        pred = pandas.concat([pred, tmwk])

pred.reset_index(inplace=True)

def_pred = pandas.merge(pred, defense, on=['Year', 'Week', 'Team'], how='inner', suffixes=['', '_real'])
