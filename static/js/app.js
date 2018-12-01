function playerStats(team) {
  d3.json(`/predict/${team}`).then((data) => {
    // Use d3 to select the panel with id of `#player-data`
    var PANELname = d3.select("#player-name");
    var PANEL = d3.select("#player-data");

    // Use `.html("") to clear any existing metadata
    PANELname.html("");
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach((player) => {
        PANELname.append("h6").text(`${player[1]['NAME']}`);
    });
    Object.entries(data).forEach((player) => {
        PANEL.append("h6").text(`PTS: ${player[1]['PTS']} REB: ${player[1]['REB']} AST: ${player[1]['AST']}`);
    });
  });
}

function playerStats2(team) {
  d3.json(`/predict/${team}`).then((data) => {
    // Use d3 to select the panel with id of `#player-data`
    var PANEL2name = d3.select("#player-name2");
    var PANEL2 = d3.select("#player-data2");

    // Use `.html("") to clear any existing metadata
    PANEL2name.html("");
    PANEL2.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    Object.entries(data).forEach((player) => {
      PANEL2name.append("h6").text(`${player[1]['NAME']}`);
    });
    Object.entries(data).forEach((player) => {
      PANEL2.append("h6").text(`PTS: ${player[1]['PTS']} REB: ${player[1]['REB']} AST: ${player[1]['AST']}`);
    });
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