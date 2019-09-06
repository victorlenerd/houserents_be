import os
import json
import psycopg2
import datetime
import numpy as np
import pandas as pd
import requests

DB_HOST = os.environ["DB_HOST"]
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_PORT = os.environ["DB_PORT"]


def populate_db(data):

    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD, port=DB_PORT)

    with conn.cursor() as curr:
        curr.execute("TRUNCATE apartments")

        for apartment in data:
            date_added = apartment['date_added'].split('T')[0]
            split_date = date_added.split('-')
            year = int(split_date[0])
            month = int(split_date[1])
            day = int(split_date[2])
            date = datetime.date(year, month, day)
            lat_lng = 'POINT({lat} {lng})'.format(lat=apartment['lat'], lng=apartment['lng'])
            curr.execute(
                """
                    INSERT INTO apartments (latLng, no_bed, no_bath, no_toilets, price, url, source, address, description, date_added)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    lat_lng,
                    apartment['no_bed'],
                    apartment['no_bath'],
                    apartment['no_toilets'],
                    apartment['price'],
                    apartment['url'],
                    apartment['source'],
                    apartment['address'],
                    apartment['description'],
                    date
                ))

        conn.commit()
        conn.close()

    return "Thank you!"


def clean_data():

    df = pd.read_json('./data.json')

    df['no_toilets'] = df['no_toilets'].astype('int32')
    df['no_bath'] = df['no_toilets'].astype('int32')
    df['no_bed'] = df['no_toilets'].astype('int32')
    df['url'] = df['url'].astype('str')
    df['source'] = df['source'].astype('str')
    df['address'] = df['address'].astype('str')
    df['description'] = df['description'].astype('str')

    df = df[(df['no_bed'] >= 1) & (df['no_toilets'] >= 1) & (df['no_bath'] >= 1)]
    df = df[(df['no_bed'] <= 10) & (df['no_bath'] <= 10) & (df['no_toilets'] <= 10)]
    df = df[df['description'] != ""]
    df = df[df['address'] != ""]
    df = df[df['price'] >= 10000]

    df = df[np.isfinite(df['lat'])]
    df = df[np.isfinite(df['lng'])]

    df = df.drop_duplicates(subset=['lat', 'lng', 'price'], keep='first')

    return populate_db(df.to_dict(orient="records"))


def download_data():

    url = '{}/data/data.json'.format(os.environ["DATA_SERVER"])

    with open('./data.json', 'w', encoding='utf-8') as dataFile:
        r = requests.get(url)
        dataFile.write(json.dumps(r.json()))
        dataFile.close()

    return clean_data()


def data_ready():

    print("Data Ready Called")
