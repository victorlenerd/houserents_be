from flask import Flask, request
from flask_request_params import bind_request_params
from dotenv import load_dotenv
import os

from controllers.home import home_controller
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

try:
    if os.environ["ENV"] == "DEV":
        template_dir = os.path.join(root_dir, 'view')
        template_dir = os.path.join(template_dir, 'public')
        static_dir = os.path.join(root_dir, 'view')
        static_dir = os.path.join(static_dir, 'public')
        static_dir = os.path.join(static_dir, 'dist')
        print("Development Environment")
    else:
        template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        template_dir = os.path.join(template_dir, 'view')
        template_dir = os.path.join(template_dir, 'build')
        static_dir = os.path.join(root_dir, 'view')
        static_dir = os.path.join(template_dir, 'assets')
except KeyError:
    print("ENV is not set")

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.before_request(bind_request_params)


@app.route('/predict', methods=['POST'])
def predict():
    return predict_controller.predict(request.data)


@app.route('/data/<date>', methods=['GET'])
def download_data(date):
    return data_controller.download_data(date)


if __name__ == '__main__':
    app.run(debug=DEBUG)
