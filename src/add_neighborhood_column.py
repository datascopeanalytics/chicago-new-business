#!/usr/bin/env python

import sys

import fiona
from shapely.geometry import mapping, shape, Point
import pyproj

import data


# read shapefile data using fiona
boundaries = {}
with fiona.drivers():
    with fiona.open(sys.argv[1]) as source:
        neighborhood_projection = pyproj.Proj(preserve_units=True, **source.crs)
        for thing in source:
            neighborhood = thing['properties']['PRI_NEIGH']
            boundaries[neighborhood] = shape(thing['geometry'])

# add the neighborhood to the row using a brute force search, which could be
# sped up computationally if necessary
reader = data.RawReader(sys.stdin)
rows = []
for row in reader:
    rows.append(row)
    row['NEIGHBORHOOD'] = ''
    if row['LONGITUDE'] and row['LATITUDE']:
        x, y = map(float, [row[k] for k in ['LONGITUDE', 'LATITUDE']])
        point = Point(neighborhood_projection(x, y))
        neighborhoods = set()
        for neighborhood, geometry in boundaries.iteritems():
            if geometry.contains(point):
                neighborhoods.add(neighborhood)
        assert len(neighborhoods) <= 1, "%s\n\n%s" % (row, neighborhoods)
        if neighborhoods:
            row['NEIGHBORHOOD'] = neighborhoods.pop()

# write the rows with the neighborhood added as the last column
fieldnames = reader.fieldnames + ['NEIGHBORHOOD']
writer = data.RawWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(rows)
