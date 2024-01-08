/**
 * Displays an error alert using SweetAlert2 (Swal) with the specified message.
 *
 * @param {string} message - The error message to display in the alert.
 */
const showErrorAlert = (message) => {
  Swal.fire({
    icon: "error",
    title: "Oops...",
    text: message,
    backdrop: "transparent",
    customClass: {
      popup: "alert-popup",
      confirmButton: "alert-confirm-button",
    },
  });
};

/**
 * Displays a success alert using SweetAlert2 (Swal) with the specified message.
 *
 * @param {string} message - The success message to display in the alert.
 */
const showSuccessAlert = (message) => {
  Swal.fire({
    icon: "success",
    title: "Success!",
    text: message,
    backdrop: "transparent",
    customClass: {
      popup: "alert-popup",
      confirmButton: "alert-confirm-button",
    },
  });
};

/**
 * Validates passwords, sends a request to reset the password, and handles the response.
 *
 * @param {Event} event - The event triggered (e.g., form submission).
 * @param {string} token - The token used for password reset.
 * @returns {boolean} - Returns true if the passwords match and the request is sent; otherwise, false.
 */
/**
 * Checks if the newPassword and confirmPassword match, and sends a password reset request if they do.
 * @param {Event} event - The event object.
 * @param {string} token - The password reset token.
 * @returns {boolean} - Returns true if the request is being processed, false otherwise.
 */
const checkPasswords = (event, token) => {
  event.preventDefault();

  // Get the values of newPassword and confirmPassword inputs
  const newPassword = document.getElementById("newPassword").value;
  const confirmPassword = document.getElementById("confirmPassword").value;

  // Check if newPassword and confirmPassword match
  if (newPassword !== confirmPassword) {
    // Display an error alert if passwords do not match
    showErrorAlert("Passwords do not match!");
    return false; // Abort further processing
  } else {
    // Passwords match, proceed to send a password reset request

    // Create an XMLHttpRequest to send a POST request
    const xhr = new XMLHttpRequest();
    xhr.open("PATCH", `${extractAddressFromURL()}/actions/reset_password/`, true);
    xhr.setRequestHeader("Content-Type", "application/json");

    // Define the callback to handle the response
    xhr.onreadystatechange = () => {
      if (xhr.readyState === 4) {
        // Check the status of the response
        if (xhr.status === 200) {
          // Display a success alert for successful password reset
          showSuccessAlert("Password reset successfully! Please close this window and Auth with your new password.");
        } else if (xhr.status === 404) {
          // Display an error alert for an invalid or expired token
          showErrorAlert("Token invalid or expired. Either you have already reset your password or you have not requested a password reset.");
        } else {
          // Display a general error alert for failed password reset
          showErrorAlert("Failed to reset password. Please try again.");
        }
      }
    };

    // Prepare the data to be sent in JSON format
    const data = JSON.stringify({ token: token, new_password: newPassword });

    // Send the request with the prepared data
    xhr.send(data);
  }
  return true; // Return true indicating that the request is being processed
};