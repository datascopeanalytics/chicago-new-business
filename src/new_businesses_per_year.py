#!/usr/bin/env python
"""
calculate the new businesses per year to make sure the numbers are sane
"""

import collections
import sys
import csv

import data

# calculate the histogram of new licenses per year
reader = data.RawReader(sys.stdin)
frequency = collections.Counter()
for row in reader:
    frequency[row.start_date.year] += 1

# print out the result
writer = csv.writer(sys.stdout)
writer.writerow(['year', 'count'])
for year, count in sorted(frequency.iteritems()):
    writer.writerow([year, count])
