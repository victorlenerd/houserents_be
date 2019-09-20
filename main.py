import os
import psycopg2
from flask import Flask, request
from flask_cors import CORS
from flask_request_params import bind_request_params
from controllers.apartments import apartments_controller
from controllers.data import data_controller
from controllers.predict import predict_controller
from misc.envs import get

app = Flask(__name__)
CORS(app)
app.before_request(bind_request_params)
envs = get()

DB_HOST = envs['DB_HOST']
DB_NAME = envs['DB_NAME']
DB_USER = envs['DB_USER']
DB_PASSWORD = envs['DB_PASSWORD']
DB_PORT = envs['DB_PORT']
PORT = envs['PORT']

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

root_dir = os.path.dirname(__file__)
sql_file_path = os.path.join(root_dir, 'db/db.sql')

with conn.cursor() as curr:
    with open(sql_file_path, 'r') as pg_sql:
        query = pg_sql.read().encode("utf8")
        curr.execute(query)
    conn.commit()

conn.close()


@app.route('/apartments', methods=['POST'])
def apartments():
    return apartments_controller.fetch_apartments(request.args['offset'], request.args['limit'], request.get_json())


@app.route('/predict', methods=['POST'])
def predict():
    return predict_controller.predict(request.get_json())


@app.route('/data/<data_file_name>', methods=['GET'])
def download_data(data_file_name):
    return data_controller.download_data(data_file_name)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(PORT))
