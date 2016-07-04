import requests

for pos in ['QB', 'RB', 'WR', 'TE', 'K']:
    for i in range(2001,2016):
        for j in range(1,18):
            u = 'https://sports.yahoo.com/nfl/stats/byposition?pos=%s&conference=NFL&year=season_%d&timeframe=Week%d&qualified=0' %(pos, i, j)
            src = requests.get(u)
            with open('Data/Raw/HTML/%s_%d_Wk%d.html' %(pos, i, j), 'w') as f:
                f.write(src.text)
