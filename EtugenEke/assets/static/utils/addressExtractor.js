/**
 * Extracts the base address from the current URL.
 * @returns {string|null} The extracted base address or null if not found.
 */
const extractAddressFromURL = () => {
    // Get the current URL
    const url = window.location.href;
  
    // Split the URL by '/' and get the first three parts (protocol, host, and port)
    const urlParts = url.split('/');
  
    // Reconstruct the base address using the protocol, host, and port
    const address = urlParts.slice(0, 3).join('/');
  
    return address || null; // Return the extracted address or null if not found
}