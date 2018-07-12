from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import os.path

model = pickle.load(open('./model.pkl', 'rb'))
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/tf_js_model/<path:path>', methods=['GET'])
def send_tf_js_model(path):
    return app.send_static_file('tf_js_model/'+path)

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