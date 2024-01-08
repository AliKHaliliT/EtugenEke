/**
 * Extracts a token from the URL query string.
 *
 * @returns {string|null} token - The extracted token from the URL query string, or null if not found.
 */
const extractTokenFromURL = () => {
  // Get the current URL
  const url = window.location.href;

  // Split the URL by '=' and return the second part (index 1)
  // This assumes the token is in the format '...?token=<value>'
  const token = url.split('=')[1];

  return token || null; // Return the extracted token or null if not found
}

// const token = extractTokenFromURL();