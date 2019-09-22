import numpy as np
import redis
import psycopg2

from flask import jsonify
from misc.envs import get

envs = get()

DB_HOST = envs["DB_HOST"]
DB_NAME = envs["DB_NAME"]
DB_USER = envs["DB_USER"]
DB_PASSWORD = envs["DB_PASSWORD"]
DB_PORT = envs["DB_PORT"]

REDIS_HOST = envs['REDIS_HOST']
REDIS_PORT = envs['REDIS_PORT']
REDIS_PASSWORD = envs['REDIS_PASSWORD']


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
