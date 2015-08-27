#!/usr/bin/env python

import sys

import data

# identify the last time these businesses renewed their licenses
reader = data.RawReader(sys.stdin)
old_locations = {}
for row in reader:
    if row.expiration_date:
        if (row.account_number not in old_locations or
            row.expiration_date > old_locations[row.account_number].expiration_date):
            old_locations[row.account_number] = row

# write it
writer = data.RawWriter(sys.stdout, fieldnames=reader.fieldnames)
writer.writeheader()
writer.writerows(old_locations.itervalues())
