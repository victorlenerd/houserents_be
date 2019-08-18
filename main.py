from flask import Flask, request
from flask_cors import CORS
from flask_request_params import bind_request_params
from dotenv import load_dotenv
import os

from controllers.apartments import apartments_controller
from controllers.data import data_controller
from controllers.predict import predict_controller

from db.connect import DBConnector

root_dir = os.path.dirname(__file__)

env_path = os.path.join(root_dir, '.env')
load_dotenv(dotenv_path=env_path)

HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]
DEBUG = os.environ["ENV"] == "DEV"

DBConnector(host=HOST, db_name=DB_NAME, db_user=DB_USER, db_password=DB_PASSWORD, db_port=DB_PORT)

print('API Server Started On Port ', DB_PORT, DB_NAME)

app = Flask(__name__)
CORS(app)
app.before_request(bind_request_params)

@app.route('/apartments', methods=['POST'])
def apartments():
    return apartments_controller.fetch_apartments(request.args['offset'], request.args['limit'], request.get_json())


@app.route('/predict', methods=['POST'])
def predict():
    return predict_controller.predict(request.get_json())


@app.route('/data', methods=['GET'])
def download_data():
    return data_controller.download_data()

if __name__ == '__main__':
    app.run(debug=DEBUG)
