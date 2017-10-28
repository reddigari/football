import pandas as pd
import requests, time
from football_utilities import get_team_abbr

url = 'http://sports.yahoo.com/nfl/players?type=position&c=NFL&pos=%s'

players = pd.DataFrame()

for pos in ['QB', 'RB', 'WR', 'TE', 'K']:
    table = None
    while table is None:
        try:
            r = requests.get(url %pos)
            tables = pd.read_html(r.text, match='Players by Position', header=1)
            table = tables[-1]
        except ValueError:
            print "Failed with url %s" %r.url

    players = pd.concat([players, table])

players.Team = players.Team.apply(lambda x: get_team_abbr(x.split()[-1]))
