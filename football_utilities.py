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
             'WAS': ['Washington', 'Redskins'],
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
             'HOU': ['Houston', 'Texans']}

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
