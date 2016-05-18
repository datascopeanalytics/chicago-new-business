#!/usr/bin/env python
import sys

import data

# identify new businesses based on the earliest time that account number has a
# business license by neighborhood
reader = data.RawReader(sys.stdin)
new_locations = {}
for row in reader:
    # Look for ISSUE aplication types only to filter out Renewals
    if row.application_type == 'ISSUE':
        # Multiple sites and location change will have ISSUE application type
        biz_key = (row.account_number, row.site_number, row.neighborhood)
        if (biz_key not in new_locations or
           row.start_date < new_locations[biz_key].start_date):
            new_locations[biz_key] = row

# write it
writer = data.RawWriter(sys.stdout, fieldnames=reader.fieldnames)
writer.writeheader()
writer.writerows(new_locations.itervalues())
