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
  });
}

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

init();