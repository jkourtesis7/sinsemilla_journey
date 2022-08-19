/*  likedislike.js
    This program sends an AJAX POST request
    to indicate a like or disklike on a comment
*/
const pre = document.querySelector('pre');

function likeHandler(event) {
	event.preventDefault();

  // Get the element that was clicked on. It's the event
  // currentTarget property.
  const element = event.currentTarget;
    // This is an <a> tag and has a readable href property
    let href = element.href;
    if(href.substr(-5)!="like/") return;
    element.href="/";

  const response = fetch(href, {
    method: 'POST',
    // Set the CSRF token header
    headers: { 'X-CSRFToken': csrftoken},
  })
    .then(response => response.text())
    .then(function(response) {
      let ht = element.innerHTML.trim();
      let sp = ht.lastIndexOf(" ");
      let val = parseInt(ht.substr(sp+1)) + 1;
      element.innerHTML = ht.substr(0, sp + 1) + val;
    });

  // Print out the result
  pre.textContent = 'URL:  ' + element.href + '\n';
}

// Select multiple classes: both like & dislike buttons
document.querySelectorAll('.like, .dislike')
	.forEach(function (link) {
		link.addEventListener('click', likeHandler);
	});
