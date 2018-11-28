from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def index():
    """return index.html"""
    return render_template("index.html")

@app.route("/data")
def get_nba_gamelog():
    import requests
    USER_AGENT = (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) ' +
        'AppleWebKit/537.36 (KHTML, like Gecko) ' +
        'Chrome/61.0.3163.100 Safari/537.36'
    )
    REQUEST_HEADERS = {
        'user-agent': USER_AGENT,
    }
    
    
    url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    
    re = requests.get(url, headers=REQUEST_HEADERS, allow_redirects=False, timeout=15)
    print(re.status_code)
    
    nba_data = re.json()
    return nba_json

if __name__ == "__main__":
    app.run()
