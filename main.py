from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import sys
from controllers.home.home_controller import HomeController
from controllers.predict.predict_controller import PredictController

load_dotenv()

try:
    root_dir = os.path.dirname(__file__)

    if os.environ["ENV"] == "DEV":
        template_dir = os.path.join(root_dir, 'view')
        template_dir = os.path.join(template_dir, 'public')
        static_dir = os.path.join(root_dir, 'view')
        static_dir = os.path.join(template_dir, 'src')
        print("Development enviroment")
    else:
        template_dir = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        template_dir = os.path.join(template_dir, 'view')
        template_dir = os.path.join(template_dir, 'build')
        static_dir = os.path.join(root_dir, 'view')
        static_dir = os.path.join(template_dir, 'assets')
except KeyError:
    print("ENV is not set")

app = Flask(__name__, template_folder=template_dir, static_url_path=static_dir)

HomeController = HomeController()
PredictController = PredictController()

@app.route('/', methods=['GET'])
def home():
    return HomeController.renderHome()

@app.route('/predict', methods=['POST'])
def predict(data):
    return PredictController.predict(data)

if __name__ == '__main__':
	app.run()