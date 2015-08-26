#!/usr/bin/env python
"""
Quick script to filter records to only those records that contain new
businesses
"""

import sys

import data

# identify new businesses
reader = data.RawReader(sys.stdin)
new_locations = {}
for row in reader:
    if (row.account_number not in new_locations or
        row.date_issued < new_locations[row.account_number].date_issued):
        new_locations[row.account_number] = row

# print out the dates really quickly
import collections
freq = collections.Counter()
for row in new_locations.itervalues():
    freq[row.date_issued.year] += 1

for k, v in sorted(freq.iteritems()):
    print k, v

# writer = data.RawWriter(sys.stdout)
# for row in new_locations.itervalues():
#     print row
