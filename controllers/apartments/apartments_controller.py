from flask import jsonify
from psycopg2.extras import RealDictCursor
from db.connect import DBConnector


def fetch_apartments(offset, limit, data):

    conn = DBConnector.instance.db_context

    no_toilets = data['specs']['no_toilets']
    no_bath = data['specs']['no_bath']
    no_bed = data['specs']['no_bed']

    lat = data['location']['lat']
    lng = data['location']['lng']

    lat_lng_point = 'POINT({} {})'.format(lat, lng)

    with conn.cursor(cursor_factory=RealDictCursor) as curr:

        result_query = """
                    SELECT address, no_bath, no_bed, no_toilets, price, source, url, views, 
                        description, date_added, ST_AsText(latlng) as latlng 
                    FROM apartments 
                    WHERE no_bed = {}
                    AND no_bath = {}
                    AND no_toilets = {}
                    AND st_dwithin(latLng, st_geomfromtext(\'{}\'), 5000)
                """.format(no_bed, no_bath, no_toilets, lat_lng_point)

        query_result_count = """
                SELECT COUNT(id)
                FROM apartments 
                WHERE no_bed = {} AND no_bath = {} AND no_toilets = {}
                AND st_dwithin(latLng, st_geomfromtext(\'{}\'), 5000)
            """.format(no_bed, no_bath, no_toilets, lat_lng_point)

        if 'filter' in data:

            if 'price_max' in data['filter']:
                max_filter = """
                            AND price <= {}
                        """.format(data['filter']['price_max'])

                result_query += max_filter
                query_result_count += max_filter

            if 'price_min' in data['filter']:
                min_filter = """
                            AND price >= {}
                        """.format(data['filter']['price_min'])

                result_query += min_filter
                query_result_count += max_filter

        result_query += "ORDER BY date_added DESC"

        if 'sort' in data:

            if 'price' in data['sort']:
                result_query += ", price {}".format(data['sort']['price'])

            if 'latLng' in data['sort']:
                result_query += ", latLng {}".format(data['sort']['latLng'])

            if 'views' in data['sort']:
                result_query += ", views {}".format(data['sort']['views'])

        result_query += """
                    OFFSET {} LIMIT {}
                """.format(offset, limit)

        curr.execute(result_query)
        records = curr.fetchall()

        curr.execute(query_result_count)
        count = curr.fetchone()['count']

    return jsonify({ "data": records, "total": count })
