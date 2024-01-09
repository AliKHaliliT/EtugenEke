const checkmarkCheck = document.querySelector(".checkmark__check");

// Function to get animation duration
/**
 * Calculates the animation duration of an element.
 * 
 * @param {HTMLElement} element - The element to calculate the animation duration for.
 * @returns {number} The animation duration in milliseconds.
 */
const getAnimationDuration = (element) => {
  const styles = window.getComputedStyle(element);
  return parseFloat(styles.animationDuration) * 1000;
}

// Wait for the checkmark__check animation to end
checkmarkCheck.addEventListener("animationend", () => {
  // A little delay for better user experience
  const animationDuration = getAnimationDuration(checkmarkCheck);
  setTimeout(() => {
      window.parent.postMessage("animationComplete", '*');
  }, animationDuration);
});
