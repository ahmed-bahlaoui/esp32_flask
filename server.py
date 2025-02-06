from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Folder to store uploaded images
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


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
    # This endpoint triggers the ESP32-CAM to take a picture
    return jsonify({"message": "Picture request sent to ESP32-CAM"}), 200


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
    print(request.headers)
    print(request.data)
