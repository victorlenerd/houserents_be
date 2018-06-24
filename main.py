from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import math


df = pd.read_csv('./data.csv')
model = pickle.load(open('./model.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def home():
      


@app.route('/predict')
def predict():
    lng = request.args['lng']
    lat = request.args['lat']
    no_bed = request.args['no_bed']
    no_bath = request.args['no_bath']
    no_toilets = request.args['no_toilets']

    loc = pd.DataFrame({
        'lng': [lng],
        'lat': [lat],
        'no_bed': [no_bed],
        'no_bath': [no_bath],
        'no_toilets': [no_toilets]
    })

    prediction = model.predict(loc)
    cost = prediction[0]

    return jsonify(price=round(cost))

@app.route('/range')
def range():
    lng = request.args['lng']
    lat = request.args['lat']
    no_bed = request.args['no_bed']
    no_bath = request.args['no_bath']
    no_toilets = request.args['no_toilets']

    high = df[(df['lng'] == float(lng)) | (df['lat'] == float(lat)) | (df['no_bath'] == int(no_bath)) | (df['no_bed'] == int(no_bed)) | (df['no_toilets'] == int(no_toilets))]['price'].quantile(0.75)
    low = df[(df['lng'] == float(lng)) | (df['lat'] == float(lat)) | (df['no_bath'] == int(no_bath)) | (df['no_bed'] == int(no_bed)) | (df['no_toilets'] == int(no_toilets))]['price'].quantile(0.25)
    
    return jsonify(low=low, high=high)

if __name__ == '__main__':
	app.run()