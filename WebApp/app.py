from flask import Flask, render_template, request, jsonify
import pickle
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.Extraction_Functions import *


model = pickle.load(open('model.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/predict', methods=['POST'])
def predict():
    url = request.form['url']
    
    if not url:
        return jsonify({'prediction': "Please provide a URL"})
    
    features = extract_features(url)
    
    prediction = model.predict(features).tolist()  # Convert ndarray to list
    
    prediction_type = get_prediction_type(prediction)
    
    return jsonify({'prediction': prediction_type})


def extract_features(url):
    url_features = {
        'url_len': len(url),
        'num_special_chars': count_special_characters(url),
        'abnormal_url': abnormal_url(url),
        'count_https': count_https(url),
        'count_http': count_http(url),
        'count_www': count_www(url),
        'digit_count': sum(c.isdigit() for c in url),
        'letter_count': sum(c.isalpha() for c in url),
        'use_of_ip': having_ip_address(url),
        'hostname_length': hostname_length(url),
        'has_shortening_service': has_shortening_service(url),
        'has_javascript_Code': has_javascript_Code(url),
        'has_Text_Encoding': check_text_encoding(url),
    }

    features_list = [value for key, value in url_features.items()]
    
    return [features_list]


def get_prediction_type(prediction):
    prediction_mapping = {
        0: "This URL is safe",
        1: "This URL is not safe"
    }
    
    return prediction_mapping.get(prediction[0], "Unknown")


if __name__ == '__main__':
    app.run(debug=True)