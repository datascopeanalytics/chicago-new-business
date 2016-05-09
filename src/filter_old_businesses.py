#!/usr/bin/env python

import sys

import data

# identify the last time these businesses renewed licenses by neighborhood
reader = data.RawReader(sys.stdin)
old_locations = {}
for row in reader:
    if row.end_date:
        # Single account can have multiple sites b/c multi location or move
        biz_key = (row.account_number, row.site_number, row.neighborhood)
        if (biz_key not in old_locations or
            row.end_date > old_locations[biz_key].end_date):
            old_locations[biz_key] = row

# write it
writer = data.RawWriter(sys.stdout, fieldnames=reader.fieldnames)
writer.writeheader()
writer.writerows(old_locations.itervalues())
