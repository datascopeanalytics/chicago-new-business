#!/usr/bin/env python
"""
quick check that the geocoding worked reasonably well
"""

import sys
import collections
import csv

import data

counts = {'unavailable': 0, 'geocoded': 0, 'not geocoded': 0}
for filename in sys.argv[1:]:
    with open(filename) as stream:
        reader = data.RawReader(stream)
        for row in reader:
            if row['LATITUDE'] and row['LONGITUDE']:
                if row['NEIGHBORHOOD']:
                    counts['geocoded'] += 1
                else:
                    counts['not geocoded'] += 1
            else:
                counts['unavailable'] += 1

writer = csv.writer(sys.stdout)
writer.writerows(counts.items())
