
# coding: utf-8

# In[1]:


#dependencies
from flask import Flask, jsonify


# In[2]:


#setup falsk app
app = Flask(__name__)


# In[3]:


@app.route("/")
def index():
    """return index.html"""
    return render_template("index.html")

def get_nba_gamelog():
    from splinter import Browser
    from bs4 import BeautifulSoup
    
    get_ipython().system('which chromedriver')
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://stats.nba.com/stats/leaguegamelog?Counter=1000&DateFrom=&DateTo=&Direction=DESC&LeagueID=00&PlayerOrTeam=P&Season=2018-19&SeasonType=Regular+Season&Sorter=DATE"
    
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    nba_data = soup.find("pre").text
    
    return jsonify(nba_data)

if __name__ == "__main__":
    app.run()
