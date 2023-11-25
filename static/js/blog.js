//     const jsonData = [
//   {
//     "heading": "\n\nFair Play Download – Netflix Original (2023) Dual Audio {Hindi-English} 480p | 720p | 1080p Movieverse \n\n",
//     "desc": "F air Play Download – Netflix Original (2023) Dual Audio {Hindi-English} 480p | 720p | 1080p Movieverse  In a world filled with complex char...Read More",
//     "link": "https://www.movieverse.art/2023/10/fair-play-download-netflix-original.html"
//   },
//   {
//     "heading": "AILET Admit Card 2023 released, here’s how to download",
//     "link": "https://www.hindustantimes.com/education/competitive-exams/ailet-admit-card-2023-releasing-today-here-s-how-to-download-101700807230786.html"
//   },
//   {
//     "heading": "\n\nFair Play Download – Netflix Original (2023) Dual Audio {Hindi-English} 480p | 720p | 1080p Movieverse \n\n",
//     "desc": "F air Play Download – Netflix Original (2023) Dual Audio {Hindi-English} 480p | 720p | 1080p Movieverse  In a world filled with complex char...Read More",
//     "link": "https://www.movieverse.art/2023/10/fair-play-download-netflix-original.html",
//     "img": "https://fujifilm-x.com/wp-content/uploads/2021/01/gfx100s_sample_01_thum.jpg"
//   }
// ];

// ... (Previous code remains the same)
function createCard(jsonData) {
const container = document.getElementById('cardsContainer');

jsonData.forEach(itemElem => {
  const card = document.createElement('div');
  card.classList.add('card');
  var item = JSON.parse(itemElem);
  console.log(item.heading);

  const imageUrl = item.img ? item.img : "../static/img/card_bg.jpg";
  const description = item.desc ? item.desc : "No desc Available";

  if (item.heading && item.link) {
  card.classList.add('cardWithDesc');
  card.innerHTML = `
    <div class="fixed-inner-card" style="background-image: url(${imageUrl})">
      <div class="text-overlay">
        <h2>${item.heading}</h2>
      </div>
      <div class="sliding-inner-card">${description}</div>
    </div>
  `;
  card.addEventListener('click', () => {
    window.open(item.link, '_blank');
  });
}
  // Add similar conditions for other cases...

  container.appendChild(card);
});
}


document.addEventListener('DOMContentLoaded', function() {

  const currentURL = window.location.href;

// Extract the path after the domain
const path = currentURL.substring(currentURL.lastIndexOf('/') + 1);

// Construct the URL for the fetch request
const fetchURL = '/fetchblog/' + path;
    // Fetch data when the page is loaded
    fetch(fetchURL)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // console.log(data);
            createCard(data);
        })
        .catch(error => {
            // Handle any errors during the fetch
            console.error('Fetch error:', error);
        });
});
// Call the createCard function with your JSON data
