from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid

from backend.utils.scoring import compare_ingredient_lists, get_profile_weights
from backend.ocr.ocr_reader import get_cleaned_ingredient_list as extract_ingredient_list_from_image

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    img1 = request.files.get('image1')
    img2 = request.files.get('image2')
    condition = request.form.get('condition', '').lower()  # Optional health condition

    if not img1 or not img2:
        return jsonify({'error': 'Please upload both images.'}), 400

    # Save uploaded files with unique names
    path1 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(uuid.uuid4()) + "_" + img1.filename))
    path2 = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(uuid.uuid4()) + "_" + img2.filename))
    img1.save(path1)
    img2.save(path2)

    # OCR step
    ingredients1 = extract_ingredient_list_from_image(path1)
    ingredients2 = extract_ingredient_list_from_image(path2)

    # If condition is 'none' or empty, treat as neutral/default
    if not condition or condition == "none":
        profile_data = get_profile_weights("default")
    else:
        profile_data = get_profile_weights(condition)

    # Compare ingredient lists
    result = compare_ingredient_lists(ingredients1, ingredients2, profile_data=profile_data)

    return jsonify({
        "recommendation": result['recommendation'],
        "score1": result['food1_score'],
        "score2": result['food2_score'],
        "similarity": result['similarity'],
        "details": result["details"]  # For 'know more' view in frontend
    })

if __name__ == '__main__':
    # For local testing and mobile connection on same Wi-Fi
    app.run(host='0.0.0.0', port=5000, debug=True)
