import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['lines.linewidth'] = 3
fontpath = '/Library/Fonts/Microsoft/cmunss.ttf'
fontprop = mpl.font_manager.FontProperties(fname=fontpath, size=16)
mpl.rcParams['font.family'] = fontprop.get_name()

data = pd.read_pickle("Data/Offense_2001-2015.pickled")

out = []
sub_data = pd.DataFrame()

active_criteria = {
    'QB': ('PsAtt', 5),
    'RB': ('RsAtt', 5),
    'WR': ('Rec', 2),
    'TE': ('Rec', 1)
}

for pos, (col, n) in active_criteria.iteritems():
    sub_data = pd.concat([sub_data, data[(data.Pos==pos) & (data[col] >= n)]])

gby = sub_data.groupby('Year')

for y in gby.groups:
    out_dict = {'year': y}
    d = gby.get_group(y)
    for pos, pos_list in zip(['QB', 'RB', 'WR', 'TE', 'Flex'], [['QB'], ['RB'], ['WR'], ['TE'], ['RB','TE','WR']]):
        out_dict[pos] = d[np.in1d(d.Pos, pos_list)].FFPts.mean()
    out.append(out_dict)

d = pd.DataFrame.from_records(out, index='year')

fig, ax = plt.subplots(figsize=(15, 10))

for pos, color in zip(['QB', 'RB', 'WR', 'TE', 'Flex'], ['red', 'blue', 'green', 'orange', 'purple']):
    vals = d[pos].values
    # ax.bar(ind, vals, width, bottom=bottoms, color=color, edgecolor='none')
    ax.plot(d.index.values, d[pos].values, color=color, label=pos)
ax.legend(loc=2, frameon=False)

for s in ['right', 'top']:
    ax.spines[s].set_visible(False)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

ax.set_xticks(np.arange(2001, 2016, 2))

plt.tight_layout()
plt.show()
