import os
import psycopg2
import datetime
import numpy as np
import pandas as pd
import boto3

from misc.envs import get

envs = get()

DB_HOST = envs["DB_HOST"]
DB_NAME = envs["DB_NAME"]
DB_USER = envs["DB_USER"]
DB_PASSWORD = envs["DB_PASSWORD"]
DB_PORT = envs["DB_PORT"]
DATA_SERVER = envs['DATA_SERVER']


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

    os.remove('./data.json')

    return "Thank you!"


def clean_data():

    df = pd.read_json('./data.json')

    print(df.head())

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


def download_data(data_file_name):
    s3 = boto3.client('s3')

    print("Fetching file", data_file_name)

    with open('./data.json', 'wb') as dataFile:
        s3.download_fileobj('houserents-data', data_file_name, dataFile)
        dataFile.close()

    return clean_data()
