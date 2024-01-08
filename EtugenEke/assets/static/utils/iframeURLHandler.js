const token = extractTokenFromURL();
const iframe = document.getElementById("resetForm");
/**
 * The source URL for the iframe with a token parameter.
 * @type {string}
 */
const iframeSrc = iframe.src + "?token=" + encodeURIComponent(token);
iframe.src = iframeSrc;