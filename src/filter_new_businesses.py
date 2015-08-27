#!/usr/bin/env python
import sys

import data

# identify new businesses based on the earliest time that account number has a
# business license in the city
reader = data.RawReader(sys.stdin)
new_locations = {}
for row in reader:
    if (row.account_number not in new_locations or
        row.date_issued < new_locations[row.account_number].date_issued):
        new_locations[row.account_number] = row

# write it
writer = data.RawWriter(sys.stdout, fieldnames=reader.fieldnames)
writer.writeheader()
writer.writerows(new_locations.itervalues())
