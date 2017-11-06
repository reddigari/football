import sys
from espnffl import FFLeague

week = int(sys.argv[1])

lg = FFLeague('BTownsFinest', 1083362)
if "--proj" in sys.argv:
    lg.get_proj(week)
lg.get_scores(week)
lg.get_rosters_and_matchup(week)
lg.output_week_vis_json(week)
if "--team-ave" in sys.argv:
    lg.output_team_vs_average_json(week)
