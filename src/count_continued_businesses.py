# !/usr/bin/env python
"""
Count continued buisnesses over the years.

Identify continued businesses:
cycling through new businesses for issue_yr, account_number, neighborhood
searching for old businesses for expiry yr (but if not found, set to "2016"),
and adding +1 for all in-between years for neighborhood
"""

import sys
import csv
import data
import collections


def load_licenses(filename, property):
    """Load in business license data."""
    businesses = {}
    with open(filename) as stream:
        reader = data.RawReader(stream)
        for row in reader:
            neighborhood = row.neighborhood
            if property == 'start_date':
                year = row.start_date.year
            elif property == 'end_date':
                if row.end_date:
                    year = row.end_date.year
                else:
                    year = 2016
            account_number = row.account_number
            site_number = row.site_number
            businesses[(account_number, site_number)] = {'neighborhood':
                                                         neighborhood,
                                                         'year':
                                                         year}
    return businesses

# read in the data
new_biz = load_licenses(sys.argv[1], 'start_date')
old_biz = load_licenses(sys.argv[2], 'end_date')

output = collections.defaultdict(int)

# Count years of continued existence (excluding issue & expiry year)
for k, v in new_biz.iteritems():
    issue_yr = new_biz[k]['year']
    neighborhood = new_biz[k]['neighborhood']
    if k in old_biz:
        expiry_yr = old_biz[k]['year']
    else:
        expiry_yr = 2016
    year = issue_yr + 1  # skip issue year to prevent double counting
    while year < expiry_yr:
        output[(neighborhood, year)] += 1
        year += 1

# write it
writer = csv.writer(sys.stdout)
writer.writerow(['neighborhood', 'year', 'continued'])

neighborhoods = list(set([new_biz[x]['neighborhood'] for x in new_biz]))
neighborhoods.sort()

for neighborhood in neighborhoods:
    years = list(set([new_biz[x]['year'] for x in new_biz]))
    years.sort()

    for year in years:
        writer.writerow([
            neighborhood,
            year,
            output[(neighborhood, year)],
        ])
