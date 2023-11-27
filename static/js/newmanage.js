
document.addEventListener("DOMContentLoaded", function () {
const userImage = document.getElementById("userImage");
const dropdown = document.getElementById("dropdown");
const logoutLink = document.getElementById("logout");

userImage.addEventListener("click", function () {
dropdown.style.display = dropdown.style.display === "none" ? "block" : "none";
});

logoutLink.addEventListener("click", function () {
// Perform logout actions here
alert("Logging out...");
});

// Close dropdown when clicking outside
window.addEventListener("click", function (event) {
if (!event.target.matches("#userImage") && !event.target.matches("#dropdown")) {
    dropdown.style.display = "none";
}
});
});

document.getElementById("testSiteBtn").addEventListener("click", function() {
        // Get form data
        const url = document.getElementById("url").value.trim();
        const parent = document.getElementById("tag1").value.trim();
        const heading = document.getElementById("tag2").value.trim();
        const desc = document.getElementById("tag3").value.trim();
        const img = document.getElementById("tag4").value.trim();
        const link = document.getElementById("tag5").value.trim();

        // Check if required fields are not empty
        if (url !== '' && parent !== '' && heading !== '') {
            // Create object with non-empty fields
            const requestData = {
                url,
                parent,
                heading
            };

            // Add other non-empty fields to the object
            if (desc !== '') requestData.desc = desc;
            if (img !== '') requestData.img = img;
            if (link !== '') requestData.link = link;

            // Send fetch request
            fetch('/testing', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
            .then(response => {
                if (response.ok) {
                    return response.json();
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                // console.log(data);
                // const jsonObject = JSON.parse(data);
                console.log(data);
                const myTestResponseText = document.getElementById('myTestResponseText');
                  const formattedResponse = JSON.stringify(data, null, 2);

  // Create a <pre> element to display the formatted JSON
  const preElement = document.createElement('pre');
  preElement.textContent = formattedResponse;

  // Append the <pre> element to the 'myTestResponseText' div
  myTestResponseText.appendChild(preElement);
                // myTestResponseText.innerText = data;

            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error.message);
            });
        } else {
            console.log('Please fill in URL, Parent, and Heading fields.');
            // Handle error message or action for missing required fields
        }
    });


