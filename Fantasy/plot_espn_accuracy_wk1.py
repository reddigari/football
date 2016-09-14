import numpy as np
import pandas as pd
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
from espnffl import FFLeague

# computer specific font settings
fontpath = '/Library/Fonts/Microsoft/cmunss.ttf'
fontprop = mpl.font_manager.FontProperties(fname=fontpath, size=16)
mpl.rcParams['font.family'] = fontprop.get_name()

lg = FFLeague('The Ocho', path=os.path.join(os.getcwd(), 'TheOcho2016'), league_id=914065)

pp = lg.merge_proj_scores(1, all_players=True)
data = pp[(pp.FFPts_proj >= 3) & (pp.FFPts_real.notnull())]
gb = data.groupby('Pos')
models = {}
fig, ax = plt.subplots(3, 2, figsize=(12, 8))

for pos, d in gb:
    m = smf.ols('FFPts_real~FFPts_proj', d).fit()
    models[pos] = m


for i, pos in enumerate(['QB', 'RB', 'WR', 'TE', 'DST', 'K']):
    ax = fig.axes[i]
    mod = models[pos]
    m, c = mod.params.FFPts_proj, mod.params.Intercept
    d = gb.get_group(pos)
    x, y = d.FFPts_proj.values, d.FFPts_real.values
    ax.scatter(x, y, facecolor='k')
    line_x = np.linspace(x.min(), x.max(), 100)
    ax.plot(line_x, m*line_x + c, 'r')
    ax.text(x=0.02, y=.98, s=r'$\mathrm{\mathsf{R^2}}$' + '= %0.3f' %mod.rsquared, transform=ax.transAxes, va='top', ha='left')
    ax.set_title(pos)

fig.suptitle('ESPN Projections vs. Performance by Position: Week 1', fontsize=16)
fig.text(0.5, 0.01, 'Projected Fantasy Points', va='bottom', ha='center', fontsize=14)
fig.text(0.05, 0.5, 'Fantasy Points', va='center', ha='left', rotation=90, fontsize=14)
plt.subplots_adjust(hspace=0.6)


sns.set_style('ticks')
sns.despine()

fig.savefig('Fantasy/Figures/espn_accuracy_wk1.png', dpi=200)
plt.show()
