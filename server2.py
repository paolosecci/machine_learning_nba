from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    """return index.html"""
    return render_template("index.html")

@app.route("/data")
def get_data():
    import requests

    nba_url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    this_user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

    re = requests.get(nba_url, headers=this_user_agent)
    print(re.status_code)
    
    import json
    nba_json = json.loads(re.text)

    return nba_json

if __name__ == "__main__":
    app.run()
