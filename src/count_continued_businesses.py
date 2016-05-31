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
import datetime


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
                    year = this_year
            account_number = row.account_number
            site_number = row.site_number
            businesses[(account_number, site_number)] = {'neighborhood':
                                                         neighborhood,
                                                         'year':
                                                         year}
    return businesses

oldest_valid_year = 2003
this_year = datetime.date.today().year

# read in the data
new_biz = load_licenses(sys.argv[1], 'start_date')
old_biz = load_licenses(sys.argv[2], 'end_date')

output = collections.defaultdict(int)

print >> sys.stderr, 'Issued: ', len(new_biz.keys())
print >> sys.stderr, 'Expiring: ', len(old_biz.keys())
# Count years of continued existence (excluding issue & expiry year)
# for k, v in new_biz.iteritems():
#     issue_yr = new_biz[k]['year']
#     neighborhood = new_biz[k]['neighborhood']
#     if k in old_biz:
#         expiry_yr = old_biz[k]['year']
#     else:
#         expiry_yr = this_year
#     year = issue_yr + 1  # skip issue year to prevent double counting
#     while year < expiry_yr:
#         output[(neighborhood, year)] += 1
#         year += 1
for k, v in old_biz.iteritems():
    expiry_yr = old_biz[k]['year']
    neighborhood = old_biz[k]['neighborhood']
    if k in new_biz:
        issue_yr = new_biz[k]['year']
    else:
        issue_yr = oldest_valid_year
    year = expiry_yr - 1  # skip expiry year to prevent double counting
    while year > issue_yr:
        output[(neighborhood, year)] += 1
        year -= 1

# write it
writer = csv.writer(sys.stdout)
writer.writerow(['neighborhood', 'year', 'continued'])

neighborhoods = list(set([new_biz[x]['neighborhood'] for x in new_biz]))
neighborhoods.sort()

for neighborhood in neighborhoods:
    years = list(set([new_biz[x]['year'] for x in new_biz] +
                     [old_biz[x]['year'] for x in old_biz]))
    years.sort()
    for year in years:
        writer.writerow([
            neighborhood,
            year,
            output[(neighborhood, year)],
        ])
