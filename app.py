from flask import Flask, jsonify, render_template
import pandas as pd
import datetime

app = Flask(__name__)

import pandas as pd
import datetime
import requests
import json
this_user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}

#FUNCTIONS
def get_data():
    nba_url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    re = requests.get(nba_url, headers=this_user_agent)
    print(re.status_code)
    nba_json = json.loads(re.text)
    return nba_json

def make_json_df(nba_json):
    headers = nba_json['resultSets'][0]['headers']
    data = nba_json['resultSets'][0]['rowSet']
    df = pd.DataFrame(data, columns=headers)
    return df

def clean_df(df):
    df = df.drop(columns=['SEASON_ID', 'PLAYER_ID', 'TEAM_ID','VIDEO_AVAILABLE'])
    df['GAME_DATE'] = df['GAME_DATE'].astype(str)
    return df

def get_time_ellapsed(str_date):
    ymd = str_date.split('-')
    y = int(ymd[0])
    m = int(ymd[1])
    d = int(ymd[2])
    then = datetime.datetime(y,m,d)
    rn = datetime.datetime.now()
    delta = rn - then
    return delta.days

def make_days_since_col(df):
    dates = df['GAME_DATE']
    days_since_arr = []
    for i in dates:
        days_since_arr.append(get_time_ellapsed(i))
    df['DAYS_SINCE_RN'] = days_since_arr
    return df

def get_team_df(team, df):
    team_df = df[df['TEAM_ABBREVIATION']==team]
    return team_df

def get_player_df(player, df):
    player_df = df[df['PLAYER_NAME']==player]
    return player_df

def get_team_json(team_abbr):
    nba_json = get_data()
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team_abbr, df)
    team_json = team_df.to_json()
    return team_json

def predict_stat(player, stat, df):
    player_df = get_player_df(player, df)
    sum_days = 0
    for num_days in player_df['DAYS_SINCE_RN']:
        sum_days += num_days
    importances = []
    for num_days in player_df['DAYS_SINCE_RN']:
        importance = ((sum_days - num_days)/sum_days)
        importances.append(importance**4)
    sum_days
    stat_ser = player_df[stat]
    stats = []
    for stat in stat_ser:
        stats.append(int(stat))
    scores = []
    for i in range(len(stats)):
        score = importances[i]*stats[i]
        scores.append(score)
    sum_importance = 0
    for imp in importances:
        sum_importance += imp
    if (sum_importance == 0):
        return sum(scores)
    else:
        p_stat = sum(scores)/sum_importance
        return round(p_stat, 2)

def predict_lineup(team_df):
    lineup_df = team_df[team_df['DAYS_SINCE_RN']<=7]
    players = lineup_df['PLAYER_NAME'].unique()
    lineup_out = {}
    for player in players:
        player_df = lineup_df[lineup_df['PLAYER_NAME'] == player]
        lineup_out[player] = player_df['MIN'].mean()
    import operator
    line_up_sorted_12 = list(reversed(sorted(lineup_out.items(), key=operator.itemgetter(1))))[:12]
    lineup = []
    for obj in line_up_sorted_12:
        lineup.append(obj[0])
    return lineup

def predict_team_stat(df, stat):
    df
    sum_days = 0
    for num_days in df['DAYS_SINCE_RN']:
        sum_days += num_days
    importances = []
    for num_days in df['DAYS_SINCE_RN']:
        importance = ((sum_days - num_days)/sum_days)
        importances.append(importance**4)
    stat_ser = df[stat]
    stats = []
    for stat in stat_ser:
        stats.append(int(stat))
    scores = []
    for i in range(len(stats)):
        score = importances[i]*stats[i]
        scores.append(score)
    sum_importance = 0
    for imp in importances:
        sum_importance += imp
    if (sum_importance == 0):
        return sum(scores)
    else:
        p_stat = sum(scores)/sum_importance
        return round(p_stat, 2)
def predict_team(t):
    with open('data/nba_team_boxscores.json') as file_in:
        nba_t_json = json.load(file_in)
    df = make_json_df(nba_t_json)
    t_df = df[df['TEAM_ABBREVIATION'] == t]
    t_games = list(t_df['GAME_ID'])
    t_match_df = df[df['GAME_ID'].isin(t_games)]
    t_opp_df = t_match_df[t_match_df['TEAM_ABBREVIATION'] != t]
    t_opp_pts = list(t_opp_df['PTS'])
    t_pts = t_df['PTS']
    while len(t_opp_pts) < len(t_df):
        t_opp_pts.append(sum(t_opp_pts)/len(t_opp_pts))
    pts_list = []
    for pts in t_df['PTS']:
        pts_list.insert(0, pts)
    t_df['pts_r'] = pts_list
    o_pts_list = []
    for o_pts in t_opp_pts:
        o_pts_list.insert(0, o_pts)
    t_df['o_pts_r'] = o_pts_list
    predicted_pts = t_df['pts_r'].ewm(alpha=.5).mean().iloc[-1]
    predicted_opp_pts = t_df['o_pts_r'].ewm(alpha=.5).mean().iloc[-1]
    return {'predicted_pts': predicted_pts, 'predicted_opp_pts': predicted_opp_pts}

@app.route("/")
def index():
    return render_template("index.html")

### CLOSED ROUTES
# @app.route("/data")
# def get_nba_json():
#     return jsonify(get_data())
# @app.route("/<team_abbr>/data")
# def get_team_data(team_abbr):
#     return jsonify(get_team_json(team_abbr))
# @app.route("/<team_abbr>/players")
# def get_team_players(team_abbr):
#     nba_json = get_data()
#     df = clean_df(make_json_df(nba_json))
#     df = make_days_since_col(df)
#     team_df = get_team_df(team_abbr, df)
#     players = team_df['PLAYER_NAME'].unique()
#     player_list = []
#     for player in players:
#         player_list.append(player)
#     return jsonify(player_list)
# @app.route("/get_teams")
# def get_teams():
#     nba_json = get_data()
#     df = clean_df(make_json_df(nba_json))
#     teams = df['TEAM_ABBREVIATION'].unique()
#     team_list = []
#     for team in teams:
#         team_list.append(team)
#     return jsonify(sorted(team_list))

@app.route("/predict/<team>")
def predict(team):
    with open('data/nba_player_boxscores.json') as file_in:
        nba_json = json.load(file_in)
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team, df)
    team_lineup = predict_lineup(team_df)
    p_json_out = []
    sum_pts = 0
    for player in team_lineup:
        p_pts = predict_stat(player, 'PTS', team_df)
        p_json_out.append({
            'NAME': player,
            'PTS': p_pts,
            'AST': predict_stat(player, 'AST', team_df),
            'REB': predict_stat(player, 'REB', team_df)
        })
        sum_pts += p_pts
    json_out = [sum_pts, p_json_out]
    return jsonify(json_out)

@app.route('/simgame/<team1>/<team2>')
def simgame(team1, team2):
    p_t1 = predict_team(team1)
    p_t2 = predict_team(team2)
    t1s = (p_t1['predicted_pts'] + p_t2['predicted_opp_pts']) / 2
    t2s = (p_t2['predicted_pts'] + p_t1['predicted_opp_pts']) / 2
    return jsonify([t1s, t2s])


if __name__ == "__main__":
    app.run(debug=True)
