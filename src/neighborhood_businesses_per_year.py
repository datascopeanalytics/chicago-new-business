#!/usr/bin/env python
import sys
import collections
import csv

import data

def aggregate_neighborhood_by_year(filename, date_attr):
    with open(filename) as stream:
        reader = data.RawReader(stream)
        counter = collections.defaultdict(collections.Counter)
        for row in reader:
            counter[row['NEIGHBORHOOD']][getattr(row, date_attr).year] +=1
    return counter


new_businesses = aggregate_neighborhood_by_year(sys.argv[1], 'start_date')
old_businesses = aggregate_neighborhood_by_year(sys.argv[2], 'end_date')

writer = csv.writer(sys.stdout)
writer.writerow(['neighborhood', 'year', 'new', 'old'])
neighborhoods = list(set(new_businesses.keys() + old_businesses.keys()))
neighborhoods.sort()
for neighborhood in neighborhoods:
    years = list(set(new_businesses[neighborhood].keys() + old_businesses[neighborhood].keys()))
    years.sort()
    for year in years:
        writer.writerow([
            neighborhood,
            year,
            new_businesses[neighborhood][year],
            old_businesses[neighborhood][year],
        ])
