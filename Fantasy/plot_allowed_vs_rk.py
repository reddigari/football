fontpath = '/Library/Fonts/Microsoft/cmunss.ttf'
fontprop = mpl.font_manager.FontProperties(fname=fontpath, size=16)
mpl.rcParams['font.family'] = fontprop.get_name()

fig1, _ = plt.subplots(4, 4, figsize=(16, 10))
fig2, _ = plt.subplots(4, 4, figsize=(16, 10))
fig3, _ = plt.subplots(4, 4, figsize=(16, 10))

for fig, var, dvar in zip([fig1, fig2, fig3], ['PsFFPtsRk', 'PsFFPtsRk', 'RsFFPtsRk'], ['PsFFPts_real', 'RcFFPts_real', 'RsFFPts_real']):
    for i, w in enumerate(range(2, 18)):
        ax = fig.axes[i]
        d = def_pred[def_pred.Week==w]
        y = d[dvar].values
        x = d[var].values
        ax.scatter(x, y, color=None, facecolor='k', alpha=0.7)
        r2 = d.corr()[var][dvar]**2
        ax.text(x=0.02, y=.98, s=r'$\mathrm{\mathsf{R^2}}$' + '= %0.3f' %r2, transform=ax.transAxes, va='top', ha='left')
        ax.text(x=0.98, y=0.02, s='Wk%d' %w, fontweight='bold', color='#630202', transform=ax.transAxes, va='bottom', ha='right')

for ax in fig1.axes + fig2.axes + fig3.axes:
    for s in ['top', 'right']:
        ax.spines[s].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

fig1.suptitle("Fantasy Points (Passing) Allowed vs. Passing Defense Rank", fontweight='bold', fontsize=16)
fig2.suptitle("Fantasy Points (Receiving) Allowed vs. Receiver Defense Rank", fontweight='bold', fontsize=16)
fig3.suptitle("Fantasy Points (Rushing) Allowed vs. Rush Defense Rank", fontweight='bold', fontsize=16)

for fig in [fig1, fig2, fig3]:
    fig.text(x=0.5, y=0.02, s="Defense's Ranking", fontweight='bold', fontsize=14, ha='center', va='bottom')
    fig.text(x=0.05, y=0.5, s="Fantasy Points Allowed", fontweight='bold', fontsize=14, ha='left', va='center', rotation=90)

fig1.savefig('Fantasy/Figures/pass_allowed_vs_rk.png', dpi=200)
fig2.savefig('Fantasy/Figures/rec_allowed_vs_rk.png', dpi=200)
fig3.savefig('Fantasy/Figures/rush_allowed_vs_rk.png', dpi=200)
