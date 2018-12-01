from flask import Flask, jsonify, render_template
import pandas as pd
import datetime

app = Flask(__name__)

#FUNCTIONS
def get_data():
    import requests
    nba_url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    this_user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
    re = requests.get(nba_url, headers=this_user_agent)
    print(re.status_code)
    import json
    nba_json = json.loads(re.text)
    return nba_json

def make_json_df(nba_json):
    headers = nba_json['resultSets'][0]['headers']
    data = nba_json['resultSets'][0]['rowSet']
    df = pd.DataFrame(data, columns=headers)
    return df

def clean_df(df):
    df = df.drop(columns=['SEASON_ID', 'PLAYER_ID', 'TEAM_ID','GAME_ID','VIDEO_AVAILABLE'])
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
        importances.append(importance**3)
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
        p_stat = sum(scores)/sum_days
        return round(p_stat, 3)
    
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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_nba_json():
    return jsonify(get_data())

@app.route("/<team_abbr>/data")
def get_team_data(team_abbr):
    return jsonify(get_team_json(team_abbr))

@app.route("/<team_abbr>/players")
def get_team_players(team_abbr):
    nba_json = get_data()
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team_abbr, df)
    players = team_df['PLAYER_NAME'].unique()
    player_list = []
    for player in players:
        player_list.append(player)
    return jsonify(player_list)

@app.route("/get_teams")
def get_teams():
    nba_json = get_data()
    df = clean_df(make_json_df(nba_json))
    teams = df['TEAM_ABBREVIATION'].unique()
    team_list = []
    for team in teams:
        team_list.append(team)
    return jsonify(sorted(team_list))

@app.route("/predict/<team>")
def predict(team):
    nba_json = get_data()
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team, df)
    team_lineup = predict_lineup(team_df)
    p_json_out = []
    for player in team_lineup:
        p_json_out.append({
            'NAME': player,
            'PTS': predict_stat(player, 'PTS', team_df),
            'AST': predict_stat(player, 'AST', team_df),
            'REB': predict_stat(player, 'REB', team_df)
        })
    return jsonify(p_json_out)
    

if __name__ == "__main__":
    app.run()
