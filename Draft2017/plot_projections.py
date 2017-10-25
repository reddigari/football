import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

raw = pd.read_csv('ffa_customrankings2017-0.csv')

N = 40
width = 0.8


for pos in ['QB', 'RB', 'WR', 'TE', 'DST']:
    posN = N
    d = raw[raw.position==pos]
    d = d.sort_values('points', ascending=False)
    if d.shape[0] >= N:
        d = d.iloc[:N, :]
    else:
        posN = d.shape[0]
    p = d.points.values
    lows = p - d.lower.values
    highs = d.upper.values - p
    min_val = np.min(d.lower.values)
    names = d.player.values

    idx = np.arange(posN)
    fig, ax = plt.subplots(figsize=(15, 8))
    ax.bar(idx + width, height=p, width=width, color='#346a00', edgecolor=None)
    ax.errorbar(idx + (1.5 * width), p, yerr=[lows, highs], fmt='none', ecolor='k')

    ax.set_xticks(idx + (1.5*width))
    ax.set_xticklabels(names, rotation=90)
    ax.set_ylabel('Projected Fantasy Points')
    ax.set_title('Top %d Projected %ss' %(N, pos))

    c = 0
    for x, v in zip(ax.get_xticks(), d.vor.values):
        s = '%0.1f' %v
        if c == 0:
            s += ' (VOR)'
        ax.text(x=x, y=5, s=s, color='white', rotation=90, ha='center', va='bottom', fontsize=8)
        c += 1

    ax.set_xlim(0, idx[-1]+3*width)
    if min_val < 1:
        bottom = min_val - 1
    else:
        bottom = 0
    ax.set_ylim(bottom=bottom)

    for s in ['right', 'top']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('left')

    plt.tight_layout()

    fig.savefig('season_projections_%s.png' %pos, dpi=200)

plt.close("all")
