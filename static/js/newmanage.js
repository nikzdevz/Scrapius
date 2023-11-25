
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
