from flask import jsonify
import json

class PredictController:
    def computeMedian(self, record):
        nums = []

        for r in record:
            nums.append(r[0])

        n = len(nums)

        if n < 1:
            return 0
        if n % 2 == 1:
            return sorted(nums)[n//2]
        else:
            return sum(sorted(nums)[n//2-1:n//2+1])/2.0

    def predict(self, data, db):

        results = []

        data = json.loads(data)
        no_toilets = data['specs']['no_toilets']
        no_bath = data['specs']['no_bath']
        no_bed = data['specs']['no_bed']

        with db.cursor() as curr:

            for d in data['locations']:
                lat_lng_point = 'POINT({} {})'.format(d['lat'], d['lng'])
                query = 'SELECT price FROM apartments WHERE st_dwithin(latLng, st_geomfromtext(\'{}\'), 1000) AND no_bed <= {} AND  no_bath <= {} AND no_toilets <= {};'.format(lat_lng_point, no_bed, no_bath, no_toilets)
                
                curr.execute(query)
                record = curr.fetchall()
                median = self.computeMedian(record)
                results.append(median)

        return jsonify(results)