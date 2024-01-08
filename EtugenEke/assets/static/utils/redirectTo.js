/**
 * Redirects to the AkAna app with the provided token.
 * If the app is not installed, falls back to a default action.
 * @param {string} token - The token to be included in the redirect URL.
 */
const redirectToAkAnaApp = (token) => {
  const appScheme = "akana://reset_password"; // Custom URL scheme for AkAna app

  // Construct the URL with query parameters (if needed)
  const appURL = `${appScheme}?token=${token}`;

  // Attempt to open the app's scheme with parameters
  window.location.href = appURL;

  // Add a timeout for handling cases where the app is not installed
  setTimeout(() => {
    // Handle the error (app not installed) or proceed with the default action
    window.location.href = `${extractAddressFromURL()}/pages/password_reset/?token=${extractTokenFromURL()}`;
  }, 2000); // Adjust timeout as needed
};
