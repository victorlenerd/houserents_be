import psycopg2
import os
import json
import datetime
from dateutil import parser

root_dir = os.path.dirname(__file__)

def connectDB(host, db_name, db_user, db_password, db_port):
    conn = psycopg2.connect(host=host, database=db_name, user=db_user, password=db_password, port=db_port)
    
    sql_file_path = os.path.join(root_dir, 'db.pgsql');
    json_file_path = os.path.join(root_dir, 'data.all.json');

    with conn.cursor() as curr:
        with open(sql_file_path, 'r') as pssql:
            query = pssql.read().encode("utf8")
            curr.execute(query)
            curr.execute('SELECT * FROM apartments')
            apartments = curr.fetchall()
            if len(apartments) == 0:
                with open(json_file_path) as json_file:
                    data = json.load(json_file)
                    for apartment in data:
                        if apartment.has_key('lat') and apartment.has_key('lng'): 
                            date_added = apartment['date_added'].split('T')[0]
                            splitdate = date_added.split('-')
                            year = int(splitdate[0])
                            month = int(splitdate[1])
                            day = int(splitdate[2])
                            date = datetime.date(year, month, day)
                            latLng = 'POINT({lat} {lng})'.format(lat=apartment['lat'], lng=apartment['lng'])
                            curr.execute("""
                                    INSERT INTO apartments (latLng, no_bed, no_bath, no_toilets, price, url, agent_phone, agent_name, date_added) 
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (
                                    latLng,
                                    apartment['no_bed'],
                                    apartment['no_bath'], 
                                    apartment['no_toilets'],
                                    apartment['price'],
                                    apartment['url'],
                                    apartment['agent_phone'],
                                    apartment['agent_name'],
                                    date
                                ))
                        conn.commit()
                    print("Apartments table populated!")

    return conn