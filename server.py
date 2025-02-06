from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ESP32-CAM IP address
ESP32_CAM_IP = "http://192.168.143.247"


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
        response = requests.get(f"{ESP32_CAM_IP}/capture")
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

    # Save the image to the uploads folder
    filename = "image.jpg"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    with open(filepath, 'wb') as f:
        f.write(image_data)

    return jsonify({"message": f"File {filename} uploaded successfully"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
