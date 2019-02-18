import pandas as pd
import numpy as np
import requests
import json
from flask import jsonify

import os

def clean_data():
    df = pd.read_json('./data.json')

    df['no_toilets'] = df['no_toilets'].astype('int32')
    df['no_bath'] = df['no_toilets'].astype('int32')
    df['no_bed'] = df['no_toilets'].astype('int32')
    df['url'] = df['url'].astype('str')
    df['address'] = df['address'].astype('str')
    df = df[(df['no_bed'] >= 1) & (df['no_toilets'] >= 1) & (df['no_bath'] >= 1)]
    df = df[(df['no_bed'] <= 10) & (df['no_bath'] <= 10) & (df['no_toilets'] <= 10)]
    df = df.drop_duplicates()

    return df.to_json(orient="records")

def download_data(date, db_context):
    url = '{}/data/{}'.format(os.environ["DATA_SERVER"], date)

    with open('./data.json', 'w', 1) as dataFile: 
        r = requests.get(url)
        dataFile.write(r.text.encode('ascii', 'ignore'))
        dataFile.close()

    return clean_data(db_context)