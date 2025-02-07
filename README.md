# **ESP32-CAM Image Capture and Display System**

![ESP32-CAM](https://geekelectronics.io/wp-content/uploads/2022/01/71LGsWic1pS._SL1500_-1.jpg)  


---

## **Overview**

This project demonstrates how to use an **AI Thinker ESP32-CAM** module to capture images and send them to a **Flask web server**. The Flask server stores the images in a folder and provides a web interface where users can:
1. Trigger the ESP32-CAM to take a picture.
2. View the most recent image dynamically on the same webpage without reloading.

The system is modular, scalable, and uses modern web technologies to provide a seamless user experience.

---

## **Table of Contents**

1. [Technologies Used](#technologies-used)
2. [System Architecture](#system-architecture)
3. [How It Works](#how-it-works)
4. [Setup Instructions](#setup-instructions)
   - [Prerequisites](#prerequisites)
   - [ESP32-CAM Setup](#esp32-cam-setup)
   - [Flask Server Setup](#flask-server-setup)
5. [Code Documentation](#code-documentation)
   - [ESP32-CAM Code](#esp32-cam-code)
   - [Flask Server Code](#flask-server-code)
   - [Frontend Code](#frontend-code)
6. [Endpoints](#endpoints)
7. [Contributing](#contributing)
8. [License](#license)

---

## **Technologies Used**

### **1. AI Thinker ESP32-CAM**
- The **ESP32-CAM** is a low-cost camera module based on the ESP32 microcontroller. It supports Wi-Fi and has a built-in OV2640 camera.
- In this project, the ESP32-CAM:
  - Connects to Wi-Fi.
  - Hosts a web server on port 80 with an endpoint (`/capture`) to trigger image capture.
  - Sends captured images to the Flask server via an HTTP POST request.

### **2. Flask**
- **Flask** is a lightweight Python web framework used to build web applications.
- In this project, Flask:
  - Serves the web interface (`index.html`).
  - Handles HTTP requests from the ESP32-CAM and the frontend.
  - Stores uploaded images in the `uploads` folder.
  - Provides endpoints for triggering image capture and retrieving the most recent image.

### **3. HTML/CSS/JavaScript**
- **HTML**: Defines the structure of the web interface.
- **CSS**: Styles the web interface for better user experience.
- **JavaScript**: Handles user interactions (e.g., button clicks) and communicates with the Flask server using AJAX (Fetch API).

### **4. AJAX (Fetch API)**
- **AJAX** allows the frontend to communicate with the backend asynchronously without reloading the page.
- In this project, AJAX is used to:
  - Trigger the ESP32-CAM to take a picture.
  - Fetch and display the most recent image dynamically.

---

## **System Architecture**

### **1. Components**
- **ESP32-CAM**:
  - Captures images when triggered by the Flask server.
  - Sends the captured image to the Flask server via an HTTP POST request.
- **Flask Server**:
  - Receives and stores images in the `uploads` folder.
  - Provides a web interface for users to interact with the system.
  - Communicates with the ESP32-CAM to trigger image capture.
- **Web Interface**:
  - Allows users to trigger image capture and view the most recent image.

### **2. Workflow**
1. The user opens the Flask web interface in their browser.
2. When the user clicks the "Take Picture" button:
   - JavaScript sends an HTTP POST request to the `/trigger` endpoint on the Flask server.
   - The Flask server sends an HTTP GET request to the ESP32-CAM's `/capture` endpoint to trigger image capture.
   - The ESP32-CAM captures an image and sends it to the Flask server via an HTTP POST request.
3. The Flask server saves the image in the `uploads` folder.
4. The JavaScript code fetches the URL of the most recent image from the `/last_image` endpoint and updates the `<img>` tag dynamically.

---

## **How It Works**

### **1. ESP32-CAM**
- The ESP32-CAM connects to Wi-Fi and hosts a web server on port 80.
- When the `/capture` endpoint is accessed:
  - The ESP32-CAM captures an image using its OV2640 camera.
  - The image is sent to the Flask server as raw binary data via an HTTP POST request.

### **2. Flask Server**
- The Flask server listens for incoming requests from the frontend and the ESP32-CAM.
- It handles the following tasks:
  - Triggers the ESP32-CAM to capture an image.
  - Receives and stores the image in the `uploads` folder.
  - Serves the web interface and dynamically updates the displayed image.

### **3. Frontend**
- The frontend is built using HTML, CSS, and JavaScript.
- When the user clicks the "Take Picture" button:
  - JavaScript sends an asynchronous request to the Flask server.
  - The Flask server triggers the ESP32-CAM to capture an image.
  - Once the image is uploaded, JavaScript fetches the URL of the most recent image and displays it dynamically.

---

## **Setup Instructions**

### **Prerequisites**
1. **Hardware**:
   - AI Thinker ESP32-CAM module.
   - Micro-USB cable for programming the ESP32-CAM.
   - Computer with VSCode and PlatformIO installed.
2. **Software**:
   - Python 3.x installed.
   - Install the required Python packages by running:
     ```bash
     pip install -r requirements.txt
     ```

### **ESP32-CAM Setup**
1. Open the ESP32-CAM code in PlatformIO and upload it to your ESP32-CAM.
2. Replace the Wi-Fi credentials (`ssid` and `password`) in the code with your network details.
3. Note the IP address of the ESP32-CAM after it connects to Wi-Fi (displayed in the serial monitor).

### **Flask Server Setup**
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/esp32-cam-flask.git
   cd esp32-cam-flask
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask server:
   ```bash
   python server.py <ESP32_CAM_IP>
   ```
   Replace `<ESP32_CAM_IP>` with the actual IP address of your ESP32-CAM.

4. Open the web interface in your browser:
   ```
   http://<FLASK_SERVER_IP>:5000/
   ```

---

## **Code Documentation**

### **ESP32-CAM Code**
- Located in `esp32_cam.ino`.
- Connects to Wi-Fi, hosts a web server, and captures images when triggered by the Flask server.
- Sends captured images to the Flask server via an HTTP POST request.

### **Flask Server Code**
- Located in `app.py`.
- Handles HTTP requests, stores images, and serves the web interface.
- Endpoints include `/`, `/trigger`, `/upload`, `/last_image`, and `/uploads/<filename>`.

### **Frontend Code**
- **HTML**: Located in `templates/index.html`.
- **CSS**: Located in `static/styles.css`.
- **JavaScript**: Located in `static/script.js`.

---

## **Endpoints**

1. **`/`**:
   - **Method**: GET
   - **Purpose**: Serves the web interface (`index.html`).

2. **`/trigger`**:
   - **Method**: POST
   - **Purpose**: Triggers the ESP32-CAM to capture an image by sending a GET request to its `/capture` endpoint.

3. **`/upload`**:
   - **Method**: POST
   - **Purpose**: Receives raw image data from the ESP32-CAM and saves it in the `uploads` folder.

4. **`/last_image`**:
   - **Method**: GET
   - **Purpose**: Returns the URL of the most recent image in the `uploads` folder.

5. **`/uploads/<filename>`**:
   - **Method**: GET
   - **Purpose**: Serves static image files from the `uploads` folder.

---

