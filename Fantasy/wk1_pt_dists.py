import pandas as pd
import matplotlib.pyplot as plt
from espnffl import *

lg = FFLeague('The Ocho', league_id=914065, path='/home/samir/Statistics/football/TheOcho2016/')

pp = lg.merge_proj_scores(1, all_players=True)
pp = pp[(pp.FFPts_proj >= 3) & (pp.FFPts_real.notnull())]
gb = pp.groupby('Pos')

positions = ['QB', 'RB', 'WR', 'TE', 'DST', 'K']

fig, ax = plt.subplots(3, 2, sharex=True)

for i, pos in enumerate(positions):
    ax = fig.axes[i]
    d = gb.get_group(pos)
    ax.hist(d.FFPts_real.values, color="grey")
    ax.set_title(pos)

plt.tight_layout()
plt.show()
