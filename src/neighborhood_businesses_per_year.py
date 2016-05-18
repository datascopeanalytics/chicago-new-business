#!/usr/bin/env python
import sys
import collections
import csv

import data


def aggregate_neighborhood_by_year(filename, date_attr):
    """Aggregate businesses by neighborhood and year."""
    with open(filename) as stream:
        reader = data.RawReader(stream)
        counter = collections.defaultdict(collections.Counter)
        for row in reader:
            counter[row['NEIGHBORHOOD']][getattr(row, date_attr).year] += 1
    return counter


def load_aggregated_data(filename):
    """Load already aggregated business data into same format."""
    with open(filename) as stream:
        reader = data.RawReader(stream)
        output = {}
        for row in reader:
            neighborhood = row['neighborhood']
            year = int(row['year'])
            count = row['continued']
            if neighborhood in output:
                output[neighborhood][year] = count
            else:
                output[neighborhood] = {}
                output[neighborhood][year] = count
    return output

new_businesses = aggregate_neighborhood_by_year(sys.argv[1], 'start_date')
old_businesses = aggregate_neighborhood_by_year(sys.argv[2], 'end_date')
# continued businesses already in neighborhood | year format
continued_businesses = load_aggregated_data(sys.argv[3])

writer = csv.writer(sys.stdout)
writer.writerow(['neighborhood', 'year', 'new', 'old', 'continued'])
neighborhoods = list(set(new_businesses.keys() + old_businesses.keys()))
neighborhoods.sort()
for neighborhood in neighborhoods:
    years = list(set(new_businesses[neighborhood].keys() +
                     old_businesses[neighborhood].keys()))
    years.sort()
    for year in years:
        if year not in continued_businesses[neighborhood].keys():
            continued_businesses[neighborhood][year] = 0
        writer.writerow([
            neighborhood,
            year,
            new_businesses[neighborhood][year],
            old_businesses[neighborhood][year],
            continued_businesses[neighborhood][year],
        ])
