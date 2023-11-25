// setTimeout(function() {
//     // Your JSON data
//     var jsonData = {
//         "totalSite": "1",
//         "totalScraped": "50",
//         "totalViews": "100",
//         "totalSubs": "5",
//         "scrapedData": {}
//     };
//
//     // Extract data
//      totalSites = jsonData.totalSite;
//     var totalScrapped = jsonData.totalScraped;
//     var totalViews = jsonData.totalViews;
//     var totalFollowers = jsonData.totalSubs;
//
//     // Hide shimmer and display data containers
//     document.getElementById('loading-sites').style.display = 'none';
//     document.getElementById('data-container-sites').style.display = 'block';
//     document.getElementById('data-container-sites').innerHTML = `<h1>${totalSites}</h1>`;
//
//     document.getElementById('loading-scrapped').style.display = 'none';
//     document.getElementById('data-container-scrapped').style.display = 'block';
//     document.getElementById('data-container-scrapped').innerHTML = `<h1>${totalScrapped}</h1>`;
//
//     document.getElementById('loading-views').style.display = 'none';
//     document.getElementById('data-container-views').style.display = 'block';
//     document.getElementById('data-container-views').innerHTML = `<h1>${totalViews}</h1>`;
//
//     document.getElementById('loading-followers').style.display = 'none';
//     document.getElementById('data-container-followers').style.display = 'block';
//     document.getElementById('data-container-followers').innerHTML = `<h1>${totalFollowers}</h1>`;
// }, 2000); // Simulating a delay of 2 seconds (you can replace this with actual code to load the JSON file)

document.addEventListener("DOMContentLoaded", function() {
    const userImage = document.getElementById("userImage");
    const dropdown = document.getElementById("dropdown");
    const logoutLink = document.getElementById("logout");

    userImage.addEventListener("click", function() {
        dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
    });

    logoutLink.addEventListener("click", function() {
        // Perform logout actions here
        alert("Logging out...");
    });

    // Close dropdown when clicking outside
    window.addEventListener("click", function(event) {
        if (!event.target.matches("#userImage") && !event.target.matches("#dropdown")) {
            dropdown.style.display = "none";
        }
    });
});

function populateTable(jsonString) {
    var tableBody = document.getElementById('table-body');

    // Clear existing rows
    tableBody.innerHTML = '';
    const data = JSON.parse(jsonString);
    // Loop through the JSON data and create table rows
    data.forEach((item) => {
        console.log(item['schema']);
        // // Extracting information from JSON
        var site = item['site'];
        var schema = item['schema'];
        var totalScraped = item['siteTotalScraped'];
        var created = item['created'];


        // Creating a new table row
        var newRow = document.createElement('tr');
        newRow.innerHTML = `<tr>
                    <td>${site}</td>
                    <td style="white-space: nowrap; max-width: 170px; overflow: hidden; text-overflow: ellipsis;">${schema}</td>
                    <td style="text-align: center;">${totalScraped}</td>
                    <td style="text-align: center;">${created}</td>
                    <td style="text-align: center;"><span class="placeholder">&nbsp;</span></td></tr>
                `;

        // Appending the new row to the table body
        tableBody.appendChild(newRow);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    // Fetch data when the page is loaded
    fetch('/fetchData')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Process the fetched data
            // console.log('Fetched data:', data);


            document.getElementById('loading-sites').style.display = 'none';
            document.getElementById('data-container-sites').style.display = 'block';
            document.getElementById('data-container-sites').innerHTML = `<h1>${data["totalSites"]}</h1>`;


            //
            document.getElementById('loading-scrapped').style.display = 'none';
            document.getElementById('data-container-scrapped').style.display = 'block';
            document.getElementById('data-container-scrapped').innerHTML = `<h1>${data["totalScraped"]}</h1>`;

            document.getElementById('loading-views').style.display = 'none';
            document.getElementById('data-container-views').style.display = 'block';
            document.getElementById('data-container-views').innerHTML = `<h1>${data["totalView"]}</h1>`;

            document.getElementById('loading-followers').style.display = 'none';
            document.getElementById('data-container-followers').style.display = 'block';
            document.getElementById('data-container-followers').innerHTML = `<h1>${data["totalSubs"]}</h1>`;

            var jsonData = data["data"];
            populateTable(jsonData);



            // Perform further actions with the data
        })
        .catch(error => {
            // Handle any errors during the fetch
            console.error('Fetch error:', error);
        });
});


function openManageSite() {
    window.open("/manageSite");
}