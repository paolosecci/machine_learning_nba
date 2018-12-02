var team1_score = 0;
var team1_name = "";
var team2_score = 0;
var team2_name = "";

function playerStats(team) {
  d3.json(`/predict/${team}`).then((data) => {
    // Use d3 to select the panel
    var PANELname = d3.select("#player-name");
    var PANEL = d3.select("#player-data");
    var PANELteam = d3.select("#team-data");

    // Use `.html("") to clear any existing data
    PANELname.html("");
    PANEL.html("");
    PANELteam.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data[1]).forEach((player) => {
        PANELname.append("h6").text(`${player[1]['NAME']}`);
    });
    Object.entries(data[1]).forEach((player) => {
        PANEL.append("h6").text(`PTS: ${player[1]['PTS']} REB: ${player[1]['REB']} AST: ${player[1]['AST']}`);
    });
    PANELteam.append("h2").text(data[0]);

    team1_score = data[0];
    team1_name = team;

  });
}

function playerStats2(team) {
  d3.json(`/predict/${team}`).then((data) => {
    // Use d3 to select the panel
    var PANEL2name = d3.select("#player-name2");
    var PANEL2 = d3.select("#player-data2");
    var PANEL2team = d3.select("#team-data2");

    // Use `.html("") to clear any existing data
    PANEL2name.html("");
    PANEL2.html("");
    PANEL2team.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data[1]).forEach((player) => {
      PANEL2name.append("h6").text(`${player[1]['NAME']}`);
    });
    Object.entries(data[1]).forEach((player) => {
      PANEL2.append("h6").text(`PTS: ${player[1]['PTS']} REB: ${player[1]['REB']} AST: ${player[1]['AST']}`);
    });
    PANEL2team.append("h2").text(data[0]);

    console.log('setting ', team, ' score');

    team2_score = data[0];

    console.log('set to ', team2_score);
    team2_name = team;

  });
}

var get_full_name = {
 "ATL": "Atlanta Hawks",
 "BKN": "Brooklyn Nets",
 "BOS": "Boston Celtics",
 "CHA": "Charolette Hornets",
 "CHI": "Chicago Bulls",
 "CLE": "Cleveland Caveliers",
 "DAL": "Dallas Mavericks",
 "DEN": "Denver Nuggets",
 "DET": "Detroit Pistons",
 "GSW": "Golden State Warriors",
 "HOU": "Houston Rockets",
 "IND": "Indiana Pacers",
 "LAC": "Los Angeles Clippers",
 "LAL": "Los Angeles Lakers",
 "MEM": "Memphis Grizzlies",
 "MIA": "Miami Heat",
 "MIL": "Milwaukee Bucks",
 "MIN": "Minnesota Timberwolves",
 "NOP": "New Orleans Pelicans",
 "NYK": "New York Knicks",
 "OKC": "Oklahoma City Thunder",
 "ORL": "Orlando Magic",
 "PHI": "Philedelphia 76ers",
 "PHX": "Phoenix Suns",
 "POR": "Portland Trail Blazers",
 "SAC": "Sacramento Kings",
 "SAS": "San Antonio Spurs",
 "TOR": "Toronto Raptors",
 "UTA": "Utah Jazz",
 "WAS": "Washington Wizards"
};

function winningteam() {
  console.log('t1s: ', team1_score);
  console.log('t2s: ', team2_score);

  if (team1_score >= team2_score) {
    winningteam = team1_name;
  } else {
    winningteam = team2_name;
  }

  var PANELwinning = d3.select("#winningteam");
  PANELwinning.html("");
  PANELwinning.append("img")
    .attr("src",'../static/img/logos/' + winningteam + '_logo.svg')
    .attr("width", 500)
    .attr("height", 500);
  PANELwinning.append("h2").text(get_full_name[winningteam]);
};

function init() {
  // Grab a reference to the dropdown select element
  var selectorFirst = d3.select("#selDataset");
  var selectorSecond = d3.select("#selDataset2");
  
  // Use the list of team abbr to populate the select options
  d3.json("/get_teams").then((teams) => {
    teams.forEach((team) => {
      selectorFirst
        .append("option")
        .text(team)
        .property("value", team);
      selectorSecond
        .append("option")
        .text(team)
        .property("value", team);
    });
  });
}

function optionChanged(newTeam) {
  playerStats(newTeam);
}
function optionChanged2(newTeam2) {
  playerStats2(newTeam2);
}

d3.selectAll("#calc").on("click", winningteam);
  
init();
