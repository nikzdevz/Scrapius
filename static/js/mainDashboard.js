let menu = document.querySelector('.menu')
let sidebar = document.querySelector('.sidebar')
let mainContent = document.querySelector('.main--content')
menu.onclick = function() {
    sidebar.classList.toggle('active')
    mainContent.classList.toggle('active')
}

let body = document.querySelector(".body")
let sun = document.querySelector(".sun")
let moon = document.querySelector(".moon")

moon.onclick = function() {
    body.classList.add("dark--mode")
}

sun.onclick = function() {
    body.classList.remove("dark--mode")
}