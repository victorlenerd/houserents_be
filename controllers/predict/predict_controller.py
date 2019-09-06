from flask import jsonify
import numpy as np
import os
from db.connect import DBConnector
from redis.redis import RedisConnector

import psycopg2

HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]


def compute_median(record):

    nums = []

    for r in record:
        nums.append(r[0])

    median_values = np.median(np.array(nums))
    removed_nan = np.nan_to_num(median_values)

    return removed_nan.tolist()


def predict(data):

    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password, port=db_port)

    results = {
        "prices": []
    }

    no_toilets = data['specs']['no_toilets']
    no_bath = data['specs']['no_bath']
    no_bed = data['specs']['no_bed']

    with conn.cursor() as curr:

        for d in data['locations']:
            lat_lng_point = 'POINT({} {})'.format(d['lat'], d['lng'])
            query = 'SELECT price FROM apartments WHERE st_dwithin(latLng, st_geomfromtext(\'{}\'), 5000) AND no_bed <= {} AND  no_bath <= {} AND no_toilets <= {};'.format(lat_lng_point, no_bed, no_bath, no_toilets)

            curr.execute(query)
            record = curr.fetchall()
            median = compute_median(record)
            results["prices"].append(median)

    conn.close()

    return jsonify(results)
