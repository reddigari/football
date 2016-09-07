import pandas
import numpy as np
from collections import OrderedDict
from itertools import chain

def agg_func(x):
    if x == 'G':
        return np.size
    else:
        return np.mean

func_dict = OrderedDict((c, agg_func(c)) for c in data.columns if c not in ['Player', 'Week', 'Pos', 'Team'])


pred = pandas.DataFrame()

for y in range(2001, 2016):
    for w in range(2, 18):
        tmp = data[(data.Year==y) & (data.Week<w)]
        plwk = tmp.groupby(['Player', 'Team', 'Pos']).agg(func_dict)
        plwk['Week'] = w
        pred = pandas.concat([pred, plwk])

pred = pred.reindex_axis(pred.columns.insert(2, 'Week')[:-1], axis=1)
pred = pred.reset_index()

qb_idx = list(chain(range(23), [-1]))
rb_idx = list(chain(range(6), range(14, 30)))
wr_idx = list(chain(range(6), range(21, 30)))

qb = data[data.Pos=='QB'].iloc[:, qb_idx]
rb = data[data.Pos=='RB'].iloc[:, rb_idx]
te = data[data.Pos=='TE'].iloc[:, rb_idx]
wr = data[data.Pos=='WR'].iloc[:, wr_idx]

qb_pred = pred[pred.Pos=='QB'].iloc[:, qb_idx]
rb_pred = pred[pred.Pos=='RB'].iloc[:, rb_idx]
te_pred = pred[pred.Pos=='TE'].iloc[:, rb_idx]
wr_pred = pred[pred.Pos=='WR'].iloc[:, wr_idx]

qb_pred = pandas.merge(qb_pred, qb, on=['Player', 'Year', 'Week', 'Team'], how='inner', suffixes=['', '_real'])
rb_pred = pandas.merge(rb_pred, rb, on=['Player', 'Year', 'Week', 'Team'], how='inner', suffixes=['', '_real'])
te_pred = pandas.merge(te_pred, te, on=['Player', 'Year', 'Week', 'Team'], how='inner', suffixes=['', '_real'])
wr_pred = pandas.merge(wr_pred, wr, on=['Player', 'Year', 'Week', 'Team'], how='inner', suffixes=['', '_real'])
