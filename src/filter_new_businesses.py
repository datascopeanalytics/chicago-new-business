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


writer = data.RawWriter(sys.stdout, fieldnames=reader.fieldnames)
writer.writeheader()
for row in new_locations.itervalues():
    writer.writerow(row)
