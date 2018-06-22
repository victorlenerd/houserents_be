from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import math

model = pickle.load(open('./model.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def home():
    lng = request.args['lng']
    lat = request.args['lat']
    no_bed = request.args['no_bed']
    no_bath = request.args['no_bath']
    no_toilets = request.args['no_toilets']

    lekki = pd.DataFrame({
        'lng': [lng],
        'lat': [lat],
        'no_bed': [no_bed],
        'no_bath': [no_bath],
        'no_toilets': [no_toilets]
    })
    prediction = model.predict(lekki)
    cost = prediction[0]

    return jsonify(price=round(cost))

if __name__ == '__main__':
	app.run()