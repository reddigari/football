def get_top_players(data):
    p = data.groupby('Player').sum()
    return p['FFPts'].nlargest(40)

gb = rb.groupby('Year')
top_rb = rb.groupby('Year').apply(get_top_players)

rbx = rb_pred.set_index(['Year', 'Player']).ix[top_rb.index.values]
rbx.index.names = ['Year', 'Player']
rbx.reset_index(inplace=True)
