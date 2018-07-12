from flask import Flask, request, render_template, jsonify, send_from_directory
import pickle
import pandas as pd
import os.path

model = pickle.load(open('./model.pkl', 'rb'))

print("Mainappp")

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('./app/build/', 'index.html')

@app.route('/static/js/<path:path>')
def send_js(path):
    return send_from_directory('./app/build/static/js', path)

@app.route('/static/css/<path:path>')
def send_css(path):
    return send_from_directory('./app/build/static/css', path)

@app.route('/static/media/<path:path>')
def send_media(path):
    return send_from_directory('./app/build/static/media', path)

@app.route('/tf_js_model/<path:path>')
def send_tf_js_model(path):
    return send_from_directory('./app/build/tf_js_model', path)

@app.route('/predict', methods=['POST'])
def predict():
    locations = request.json['locations']
    specs = request.json['specs']

    data = []

    for location in locations:
        data.append({
            'lat': location['lat'],
            'lng': location['lng'],
            'no_bed': specs['no_bed'],
            'no_bath': specs['no_bath'],
            'no_toilets': specs['no_toilets']
        })

    loc = pd.DataFrame(data)

    prediction = model.predict(loc)

    return jsonify(prices=prediction.tolist())

if __name__ == '__main__':
	app.run()