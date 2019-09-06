from flask import jsonify
import numpy as np
import os
import redis
import psycopg2

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]

REDIS_HOST = os.environ['REDIS_HOST']
REDIS_PORT = os.environ['REDIS_PORT']
REDIS_PASSWORD = os.environ['REDIS_PASSWORD']


def compute_median(record):

    nums = []

    for r in record:
        nums.append(r[0])

    median_values = np.median(np.array(nums))
    removed_nan = np.nan_to_num(median_values)

    return removed_nan.tolist()


def predict(data):

    results = {
        "prices": []
    }

    if 'no_bed' in data and 'locations' in data:
        no_bed = data['no_bed']
        locations = data['locations']
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

        with conn.cursor() as curr:

            for d in locations:

                query_key = '{}:{}:{}'.format(d['lat'], d['lng'], no_bed)
                loc_avg = r.get(query_key)

                if loc_avg is None:
                    lat_lng_point = 'POINT({} {})'.format(d['lat'], d['lng'])
                    query = 'SELECT price FROM apartments WHERE st_dwithin(latLng, st_geomfromtext(\'{}\'), 5000) AND no_bed = {} ;'.format(lat_lng_point, no_bed)

                    curr.execute(query)
                    record = curr.fetchall()
                    median = compute_median(record)
                    r.set(query_key, median, ex=1209600)
                    results["prices"].append(median)
                else:
                    results["prices"].append(float(str(loc_avg.decode('utf-8'))))

        conn.close()
    else:
        return jsonify(results)

    return jsonify(results)
