from flask import Flask, request, jsonify, render_template
import os
import cv2
from paddleocr import PaddleOCR

app = Flask(__name__)

def scan_plate_with_paddleocr(image):
    ocr = PaddleOCR(use_gpu=False, lang='en')
    results = ocr.ocr(image, cls=True)
    if results and len(results[0]) > 0:
        plate_number = ''.join(filter(str.isalnum, results[0][0][1][0]))
        return plate_number[:8]
    return "UNKNOWN"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    image_path = os.path.join("uploads", image_file.filename)
    os.makedirs("uploads", exist_ok=True)
    image_file.save(image_path)

    # Process the image
    plate = cv2.imread(image_path)
    plate_number = scan_plate_with_paddleocr(plate)

    return jsonify({"plate_number": plate_number})

if __name__ == "__main__":
    app.run(debug=True)
