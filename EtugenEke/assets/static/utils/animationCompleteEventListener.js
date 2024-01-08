/**
 * Listens for a "message" event and redirects to the AkAna app
 * when the event data is "animationComplete".
 * @param {string} token - The token extracted from the URL.
 */
window.addEventListener("message", (event) => {
  if (event.data === "animationComplete") {
    redirectToAkAnaApp(extractTokenFromURL());  
  }
});