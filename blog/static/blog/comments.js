/* blog/static/blog/comments.js */

const commentForm = document.querySelector('#comment-form');

async function commentFormSubmitHandler(event) {
  // Prevent submission
  event.preventDefault();

  // Get the form action attribute (URL to post to)
  const apiUrl = commentForm.action;

  // Create a FormData instance with entered data
  const formData = new FormData(commentForm);

  // Post comment to server using AJAX
  const response = await fetch(apiUrl, {
    method: 'POST',
    body: formData,
  });

  if (response.ok) {
    // Hide the form
    commentForm.hidden = true;

    // Create a success message and display
    const successMessage = document.createElement('p');
    successMessage.textContent = 'Your comment was sent!'
    commentForm.parentNode.append(successMessage);
  } else {
    const errorMessage = document.createElement('p');
    errorMessage.textContent = 'An error occurred. Please try again.'
    commentForm.parentNode.append(errorMessage);
  }
}

commentForm.addEventListener('submit', commentFormSubmitHandler);
