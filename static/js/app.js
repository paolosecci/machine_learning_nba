function playerStats(team) {
  d3.json(`/<team_abbr>/players`).then((data) => {
    // Use d3 to select the panel with id of `#sample-metadata`
    var PANEL = d3.select("#player-data");

    // Use `.html("") to clear any existing metadata
    PANEL.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(data).forEach((player) => {
      PANEL.append("h6").text(`${player}`);
    });

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of team abbr to populate the select options
  d3.json("/get_teams").then((teams) => {
    teams.forEach((team) => {
      selector
        .append("option")
        .text(team)
        .property("value", team);
    });

    const firstTeam = teams[0];
    buildMetadata(firstTeam);
  });
}

function optionChanged(newTeam) {

  playerStats(newTeam);
}

init();
