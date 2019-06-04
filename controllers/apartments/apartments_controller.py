from flask import jsonify
from psycopg2.extras import RealDictCursor

from db.connect import DBConnector


def fetch_apartments(offset, limit, data):

    conn = DBConnector.instance.db_context

    no_toilets = data['specs']['no_toilets']
    no_bath = data['specs']['no_bath']
    no_bed = data['specs']['no_bed']

    with conn.cursor(cursor_factory=RealDictCursor) as curr:
        query = """
                    SELECT address, no_bath, no_bed, no_toilets, price, source, url, 
                        description, date_added, ST_AsText(latlng) as latlng 
                    FROM apartments 
                    WHERE no_bed = {} AND no_bath = {} AND no_toilets = {}
                    ORDER BY date_added DESC
                    OFFSET {} LIMIT {}
                """.format(no_bed, no_bath, no_toilets, offset, limit)

        curr.execute(query)
        record = curr.fetchall()

    return jsonify(record)
