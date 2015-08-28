#!/usr/bin/env python

import csv
import sys

import figs

def load_counts(filename):
    counts = {}
    with open(filename) as stream:
        stream.readline()
        reader = csv.reader(stream)
        for row in reader:
            year, count = map(int, row)
            counts[year] = count
    return counts

# read in the data
new_counts = load_counts(sys.argv[1])
old_counts = load_counts(sys.argv[2])
year_range = range(2004, 2015)
new_counts = [new_counts[year] for year in year_range]
old_counts = [-old_counts[year] for year in year_range]

fig = figs.FlowOverTime(year_range, new_counts, old_counts)
fig.save(sys.argv[-1])
