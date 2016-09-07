import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('Data/Offense_2001-2015.csv')

d = data.groupby(['Year', 'Player', 'Pos']).sum().reset_index()

d = d[['Year', 'Player', 'Pos', 'FFPts']]
d_pred = d.copy()
d_pred['Year'] += 1

d = pd.merge(d_pred, d, on=['Year', 'Player', 'Pos'], how='inner', suffixes=['_last', ''])

pred = d[d.FFPts_last >= 50]

fig, _ = plt.subplots(2, 2, figsize=(16, 16))

for i, pos in enumerate(['QB', 'RB', 'WR', 'TE']):
    ax = fig.axes[i]
    x = pred[pred.Pos==pos]
    ax.scatter(x.FFPts_last.values, x.FFPts.values, facecolor='k', color='none')
    ax.set_ylim(bottom=0)
    r2 = x.corr()['FFPts_last']['FFPts']**2
    ax.text(x=0.02, y=.98, s=r'$\mathrm{\mathsf{R^2}}$' + '= %0.3f' %r2, transform=ax.transAxes, va='top', ha='left')

plt.show()
