from flask import Flask, render_template, request, jsonify
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
    return '''
    <html>
        <body>
            <h1>ESP32-CAM Picture Capture</h1>
            <form action="/trigger" method="POST">
                <button type="submit">Take Picture</button>
            </form>
        </body>
    </html>
    '''


@app.route('/trigger', methods=['POST'])
def trigger():
    # Trigger the ESP32-CAM to take a picture
    try:
        response = requests.get(f"http://{ESP32_CAM_IP}/capture")
        if response.status_code == 200:
            return jsonify({"message": "Picture captured and sent successfully"}), 200
        else:
            return jsonify({"error": f"Failed to trigger ESP32-CAM: {response.text}"}), 500
    except Exception as e:
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
