from flask import jsonify
from psycopg2.extras import RealDictCursor
from db.connect import DBConnector


def fetch_apartments(offset, limit, data):

    conn = DBConnector.instance.db_context

    no_bed = data['specs']['no_bed']

    lat = data['location']['lat']
    lng = data['location']['lng']

    lat_lng_point = 'POINT({} {})'.format(lat, lng)

    with conn.cursor(cursor_factory=RealDictCursor) as curr:

        result_query_params = [no_bed, lat_lng_point]
        count_query_params = [no_bed, lat_lng_point]

        result_query = """
                    SELECT address, no_bath, no_bed, no_toilets, price, source, url, views, 
                        description, date_added, ST_AsText(latlng) as latlng 
                    FROM apartments 
                    WHERE no_bed = %s
                    AND st_dwithin(latLng, st_geomfromtext(%s), 5000)
                """

        query_result_count = """
                SELECT COUNT(id)
                FROM apartments 
                WHERE no_bed = %s
                AND st_dwithin(latLng, st_geomfromtext(%s), 5000)
            """

        if 'filter' in data:

            if 'max_price' in data['filter'] and data['filter']['max_price'] > 0:
                max_filter = "AND price <= %s"

                result_query += max_filter
                query_result_count += max_filter

                result_query_params.append(data['filter']['max_price'])
                count_query_params.append(data['filter']['max_price'])

            if 'min_price' in data['filter'] and data['filter']['min_price'] > 0:
                min_filter = "AND price >= %s"

                result_query += min_filter
                query_result_count += min_filter

                result_query_params.append(data['filter']['min_price'])
                count_query_params.append(data['filter']['min_price'])

        if 'sort' in data and data['sort'] == 'recent':
            result_query += " ORDER BY date_added DESC"
        elif 'sort' in data and data['sort'] == 'price':
            result_query += " ORDER BY price DESC"

        if limit != 'all':
            result_query += " OFFSET %s "
            result_query_params.append(offset)

            result_query += "LIMIT %s"
            result_query_params.append(limit)

        print(result_query, result_query_params)

        curr.execute(result_query, result_query_params)
        records = curr.fetchall()

        curr.execute(query_result_count, count_query_params)
        count = curr.fetchone()['count']

    return jsonify({"data": records, "total": count})


