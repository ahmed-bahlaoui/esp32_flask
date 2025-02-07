document.getElementById("capture-btn").addEventListener("click", function () {
  // Show the notification
  const notification = document.getElementById("notification");
  notification.style.display = "block"; // Make the notification visible

  // Hide the notification after 2 seconds
  setTimeout(() => {
    notification.style.display = "none"; // Hide the notification
  }, 2000); // 2000ms = 2 seconds

  // Trigger the ESP32-CAM to take a picture
  fetch("/trigger", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      // Update the result message
      document.getElementById("result").innerText = data.message || data.error;

      // Fetch and display the last image
      fetch("/last_image")
        .then((response) => {
          if (!response.ok) {
            throw new Error("No images found");
          }
          return response.json();
        })
        .then((data) => {
          const imgElement = document.getElementById("last-image");
          imgElement.src = data.image_url; // Set the image source
          imgElement.style.display = "block"; // Show the image
        })
        .catch((error) => {
          document.getElementById("result").innerText =
            "Error fetching image: " + error.message;
        });
    })
    .catch((error) => {
      document.getElementById("result").innerText = "Error: " + error;
    });
});
