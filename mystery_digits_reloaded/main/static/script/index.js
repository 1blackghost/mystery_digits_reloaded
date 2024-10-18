function viewleader(){
    let o = document.getElementById("over").style;
    o.display = "block";
}

function clo(){
    let o = document.getElementById("over").style;
    o.display = "none";
}

$(document).ready(function() {
    // Function to get and display leaderboard
    function getLeaderboard() {
        $.ajax({
            type: 'GET',
            url: '/getL',
            success: function(response) {
                console.log("Success. Response:", response);

                // Clear existing leaderboard rows
                $("#leaderboardBody").empty();

                // Check if the response is an array
                if (Array.isArray(response)) {
                    // Add new rows to the leaderboard table
                    $.each(response, function(index, entry) {
                        // Check if the eliminated field is '1'
                        var rowClass = entry[4] === '1' ? 'eliminated' : '';  // entry[4] is the eliminated field
                        var crossMark = entry[4] === '1' ? ' ❌' : '';  // Add cross mark if eliminated

                        // Append new row to leaderboard body
                        $("#leaderboardBody").append(
                            "<tr class='" + rowClass + "'><td>" + entry[0] + "</td>" +  // Rank
                            "<td>" + crossMark + entry[1] + "</td>" +                   // Name with cross mark if eliminated
                            "<td>" + entry[2] + "</td>" +                               // Level
                            "<td>" + entry[3] + "</td>" +                               // Average Time
                            "</tr>"
                        );
                    });
                } else {
                    console.error("Invalid response format. Expected an array.");
                }
            },
            error: function(error) {
                console.error("Error fetching leaderboard: ", error);
            }
        });
    }

    // Function to check for changes
    function checkForChanges() {
        $.ajax({
            type: 'GET',
            url: '/changesL',
            success: function(response) {
                console.log("Changes check response:", response);
                if (response.data === 1) {
                    getLeaderboard(); // If data is 1, fetch the leaderboard
                } else {
                    console.log("No changes detected, skipping leaderboard update.");
                }
            },
            error: function(error) {
                console.error("Error checking for changes: ", error);
            }
        });
    }

    // Call the function to get and display the leaderboard on page load
    getLeaderboard();
    // Set up interval to check for changes every 2 seconds
    setInterval(checkForChanges, 2000); // Adjust the interval as needed
});
