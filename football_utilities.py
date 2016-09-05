import re

short_dict = {'DEN': ['Denver', 'Broncos'],
             'MIA': ['Miami', 'Dolphins'],
             'GNB': ['Green Bay', 'Packers', 'GB'],
             'JAC': ['Jacksonville', 'Jaguars', 'JAX'],
             'NOR': ['New Orleans', 'Saints', 'NO'],
             'NYJ': ['Jets'],
             'BAL': ['Baltimore', 'Ravens'],
             'NYG': ['Giants'],
             'CIN': ['Cincinnati', 'Bengals'],
             'OAK': ['Oakland', 'Raiders'],
             'NWE': ['New England', 'Patriots', 'NE'],
             'PHI': ['Philadelphia', 'Eagles'],
             'CAR': ['Carolina', 'Panthers'],
             'SFO': ['San Francisco', '49ers', 'SF'],
             'IND': ['Indianapolis', 'Colts'],
             'ATL': ['Atlanta', 'Falcons'],
             'LAR': ['Los Angeles', 'Rams', 'St. Louis', 'Saint Louis', 'STL', 'LA'],
             'TAM': ['Tampa Bay', 'Tampa', 'Buccaneers', 'Bucs', 'TB'],
             'KAN': ['Kansas City', 'Kansas', 'Chiefs', 'KC'],
             'WAS': ['Washington', 'Redskins', 'WSH'],
             'CLE': ['Cleveland', 'Browns'],
             'TEN': ['Tennessee', 'Titans'],
             'DET': ['Detroit', 'Lions'],
             'MIN': ['Minnesota', 'Vikings'],
             'SEA': ['Seattle', 'Seahawks'],
             'PIT': ['Pittsburgh', 'Steelers'],
             'CHI': ['Chicago', 'Bears'],
             'SDG': ['San Diego', 'Chargers', 'SD'],
             'BUF': ['Buffalo', 'Bills'],
             'DAL': ['Dallas', 'Cowboys'],
             'ARI': ['Arizona', 'Cardinals'],
             'HOU': ['Houston', 'Texans'],
             'FA': ['Free Agent', 'Free', 'Agent']}

team_dict = {}

for team, shorts in short_dict.iteritems():
    for name in shorts:
        team_dict[name.upper()] = team

def get_team_abbr(x):
    x = x.upper()
    if x in team_dict.values():
        return x
    else:
        return team_dict[x]

def get_opp_from_row(r, schgb):
    """schgb is the full schedule grouped by year and week"""
    s = schgb.get_group((r['Year'], r['Week']))
    gameid = s.loc[s.GameID.str.match('.*%s.*' %r['Team']), 'GameID'].values[0]
    if gameid.startswith(r['Team']):
        return gameid[4:7]
    else:
        return gameid[0:3]

def split_espn_plr(x, out='name'):
    output = {}
    split = x.split(', ')
    if len(split) > 1:
        output['name'] = split[0]
        output['team'] = get_team_abbr(split[1].split(u'\xa0')[0])
        output['pos'] = split[1].split(u'\xa0')[1]
    else:
        output['name'] = split[0].split(' ')[0]
        output['team'] = get_team_abbr(output['name'])
        output['pos'] = 'DST'
    output['name'] = output['name'].replace('*', '')
    return output[out]
