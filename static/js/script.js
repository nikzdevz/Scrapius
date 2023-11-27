const wrapper = document.querySelector('.wrapper');
const fillScreen = document.querySelector('.fillScreen');
const loginLink = document.querySelector('.login-link');
const registerLink = document.querySelector('.register-link');
const btnPopup = document.querySelector('.btnLogin-popup');
const iconClose = document.querySelector('.icon-close');

registerLink.addEventListener('click', ()=> {
    wrapper.classList.add('active');
    // fillScreen.classList.add('active');
});

loginLink.addEventListener('click', ()=> {
    wrapper.classList.remove('active');
});

btnPopup.addEventListener('click', ()=> {
    wrapper.classList.add('active-popup');
    fillScreen.classList.add('active');

});

iconClose.addEventListener('click', ()=> {
    wrapper.classList.remove('active-popup');
    fillScreen.classList.remove('active');
});

document.addEventListener('DOMContentLoaded', function() {
    // Replace 'animation.json' with the path to your Lottie JSON file
    const animationPath = 'static/img/Animation.json';

    // Get a reference to the container
    const container = document.getElementById('lottie-container');

    // Load the animation
    const animData = {
        container: container,
        renderer: 'svg', // Choose the renderer (svg, canvas, html)
        loop: true,
        autoplay: true,
        path: animationPath // Path to your JSON file
    };

    // Display the animation
    const anim = lottie.loadAnimation(animData);
});
