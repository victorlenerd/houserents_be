from flask import request, jsonify
import pickle
import os

root_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class PredictController:
    def predict(self, data):
        pass