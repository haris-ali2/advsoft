from flask import Flask, request, jsonify
import cv2
import numpy as np

# Initialize the Flask application
app = Flask(__name__)

# Route HTTP posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400

    file = request.files['image']
    
    # Convert the file to an OpenCV image
    in_memory_file = np.frombuffer(file.read(), dtype=np.uint8)
    image = cv2.imdecode(in_memory_file, cv2.IMREAD_COLOR)
    
    if image is None:
        return jsonify({'error': 'Failed to decode image'}), 400
    
    # Save the received image for debugging
    # cv2.imwrite('received_image.jpg', image)

    bd = cv2.barcode.BarcodeDetector()
    retval, _, _ = bd.detectAndDecode(image)
    
    if len(retval):
        barcodes = retval
    else:
        barcodes = ['No barcode found!']

    return jsonify({'barcodes': barcodes})

if __name__ == '__main__':
    app.run()
