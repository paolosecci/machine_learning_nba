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

def get_team_df(team):
    team_df = df[df['TEAM_ABBREVIATION']==team]
    return team_df

def get_player_df(player):
    player_df = df[df['PLAYER_NAME']==player]
    return player_df

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    return jsonify(get_data())

@app.route("/<team_abbr>")
def get_team_data(team_abbr):
    nba_json = get_data()
    df = clean_df(make_json_df(nba_json))
    df = make_days_since_col(df)
    team_df = get_team_df(team_abbr)
    team_json = team_df.to_json()
    return jsonify(team_json)

if __name__ == "__main__":
    app.run()