document.getElementById("capture-btn").addEventListener("click", function () {
  // Send an AJAX POST request to the /trigger endpoint
  fetch("/trigger", { method: "POST" })
    .then((response) => response.json())
    .then((data) => {
      // Update the result message
      document.getElementById("result").innerText = data.message || data.error;

      // Fetch the URL of the last image
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
