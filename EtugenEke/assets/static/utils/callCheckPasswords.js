document.addEventListener('DOMContentLoaded', function() {
  // Add event listener to the form
  /**
   * Represents the form element.
   * @type {HTMLFormElement}
   */
  var form = document.querySelector('form');
  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission
    
    // Call your functions here
    checkPasswords(event, extractTokenFromURL());
  });
});
  