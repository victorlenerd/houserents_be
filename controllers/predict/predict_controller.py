from flask import request, jsonify
import pickle
import numpy
import pandas as pd
import os

root_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

model = pickle.load(open(os.path.join(root_dir, 'predict/model.pkl'), 'rb'))

class PredictController:
    def predict(self, data):
        locations = request.json['locations']
        sqpecs = request.json['specs']

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

