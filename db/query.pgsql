SELECT price FROM apartments WHERE st_dwithin(latlng, st_geomfromtext('POINT(6.4698 3.5852)'), 500) AND no_bed = 2 AND no_bath = 2 AND no_toilets = 2