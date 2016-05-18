"""
Use Google Maps Geocoding API.

Assign missing Lat|Lng to business addresses.
"""
# !/usr/bin/env python
# -*- coding: utf8 -*-
import sys

import pandas as pd
import re
import requests
import google_api


class APIError(Exception):
    """Generic error from Google API."""

    pass


class OverQueryLimit(APIError):
    """You are over your API query limit."""

    pass


def copy_missing_rows(df, column):
    """Return copy of df missing values in passed column."""
    return df[pd.isnull(df[column])].copy()


def strip_end_noise(str):
    """Remove junk from end of addresses."""
    return str.split("#")[0].split('&')[0].split(',')[0].split('/')[0].strip()


def end_has_numbers(inputString):
    """Remove last element in address if it contains number."""
    if len(inputString) == 0:
        return False
    else:
        return bool(re.search(r'\d', inputString.split()[-1]))


def end_is_single_char(inputString):
    """Remove last element in address if 1 element long."""
    if len(inputString) == 0:
        return False
    else:
        return bool(len(inputString.split()[-1]) <= 1)


def clean_addr(address):
    """Remove trailing noise from address (e.g., apartment numbers, letters).

    Also, replace nonsense in address.
    """
    address = strip_end_noise(address)
    if end_has_numbers(address):
        address = ' '.join(address.split()[:-1])
    if end_is_single_char(address):
        address = ' '.join(address.split()[:-1])
    address.replace('PKWY', 'PARKWAY').replace('AVE RD', 'AVE').replace(
                    'AVE AVE', 'AVE')
    return address


def unique_clean_street_addresses(df):
    """Add CLEAN_ADDRESS to be used for API. Drop duplicates."""
    df['CLEAN_ADDRESS'] = df['ADDRESS'].apply(lambda x: clean_addr(x))
    df = df.drop_duplicates('CLEAN_ADDRESS').copy()
    return df


def get_request(street, city, state, key):
    """Make API call and return request for passed params."""
    url = 'https://maps.googleapis.com/maps/api/geocode/json?address='\
          + street + ',' + city + ',' + state + '&key=' + key
    return requests.get(url)


def extract_lat_lng(r):
    """Extract and return latitue and longitude from API response."""
    lat = r.json()['results'][0]['geometry']['location']['lat']
    lng = r.json()['results'][0]['geometry']['location']['lng']
    return lat, lng


def make_address_request(street, city, state, key):
    """Make API request for passed params. Final clean of street address."""
    street = street.replace('  ', '+').replace(' ', '+')
    return get_request(street, city, state, key)


def store_lat_lng(df, address_dict, match_col='CLEAN_ADDRESS'):
    """Store LATITUDE and LONGITUDE in dataframe."""
    for k, v in address_dict.iteritems():
        df.loc[df[match_col] == k, 'LATITUDE'] = v[0]
        df.loc[df[match_col] == k, 'LONGITUDE'] = v[1]


def add_missing_latlng(df, source_df):
    """Assign Lat| Lng from source_df to df where address columns match."""
    df.loc[df.ADDRESS.isin(source_df.ADDRESS),
           ['LATITUDE', 'LONGITUDE']] = source_df[['LATITUDE', 'LONGITUDE']]


# Retrieve API key from config file
key = google_api.google_api_key
# Load in raw business
df = pd.read_csv(sys.stdin, low_memory=False)
missing_latlng_df = copy_missing_rows(df, 'LOCATION')
missing_latlng_df = unique_clean_street_addresses(missing_latlng_df)

# Clean addresses to send to API for LAT | LNG
# clean_addr_set = set(missing_latlng_df.CLEAN_ADDRESS)
clean_addr_set = missing_latlng_df.CLEAN_ADDRESS

# Make dictionary to store address to lat|lng mapping
addr_to_coordinate_dict = {}
# API call to retrieve lat lng for each clean addr
for addr in clean_addr_set:
    # skip blank, else api wiil return chicago, il lat|lng
    if addr == '':
        continue
    street = addr
    city = 'CHICAGO'
    state = 'IL'
    # Call API
    r = make_address_request(street, city, state, key)
    # Check if over API limit
    if r.json()['status'] == 'OVER_QUERY_LIMIT':
        # SAVE Original INPUT as OUTPUT
        df.to_csv(sys.stdout, index=False)
        msg = 'Congrats! You and your team have exceeded the daily request '\
              'quota for Google\'s API. Try again tomorrow '\
              '\xc2\xaf\\_(\xe3\x83\x84)_/\xc2\xaf'  # shrug
        raise OverQueryLimit(msg)
        # break
    else:
        if r.json()['status'] != 'OK':
            print >> sys.stderr,  r.json()['status']
        lat, lng = extract_lat_lng(r)
        addr_to_coordinate_dict[addr] = [lat, lng]

store_lat_lng(missing_latlng_df, addr_to_coordinate_dict)
# Assign Lat| Lng to original df where address columns match
add_missing_latlng(df, missing_latlng_df)

# SAVE OUTPUT
df.to_csv(sys.stdout, index=False)
