from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import time  # For generating timestamps
import requests
import sys  # For handling command-line arguments

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Check if the ESP32-CAM IP address is provided as a command-line argument
if len(sys.argv) < 2:
    print("Usage: python app.py <ESP32_CAM_IP>")
    sys.exit(1)

# Get the ESP32-CAM IP address from the first argument
ESP32_CAM_IP = sys.argv[1]


@app.route('/')
def index():
    return render_template('index.html')  # Serve the external HTML file


@app.route('/trigger', methods=['POST'])
def trigger():
    try:
        # Send a GET request to the ESP32-CAM's /capture endpoint
        response = requests.get(f"http://{ESP32_CAM_IP}/capture")

        # Log the response for debugging
        print(f"ESP32-CAM Response: {response.status_code}, {response.text}")

        if response.status_code == 200:
            return jsonify({"message": "Picture captured and sent successfully"}), 200
        else:
            return jsonify({"error": f"Failed to trigger ESP32-CAM: {response.text}"}), 500
    except Exception as e:
        # Log the exception for debugging
        print(f"Error triggering ESP32-CAM: {str(e)}")
        return jsonify({"error": f"Error triggering ESP32-CAM: {str(e)}"}), 500


@app.route('/upload', methods=['POST'])
def upload():
    # Read raw image data from the request body
    image_data = request.data
    if not image_data:
        return jsonify({"error": "No image data received"}), 400

    # Generate a unique filename using a timestamp
    timestamp = int(time.time())  # Current Unix timestamp
    filename = f"image_{timestamp}.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Save the image to the uploads folder
    with open(filepath, 'wb') as f:
        f.write(image_data)

    return jsonify({"message": f"File {filename} uploaded successfully"}), 200


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/last_image')
def last_image():
    # Get the list of files in the uploads folder
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        return jsonify({"error": "No images found"}), 404

    # Sort files by modification time (most recent first)
    files.sort(key=lambda x: os.path.getmtime(
        os.path.join(app.config['UPLOAD_FOLDER'], x)), reverse=True)
    last_image_name = files[0]

    # Return the URL of the most recent image
    return jsonify({"image_url": f"/uploads/{last_image_name}"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
