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


def add_clean_street_address(df):
    """Return df with new column for CLEAN_ADDRESS to be used for API."""
    df['CLEAN_ADDRESS'] = df['ADDRESS'].apply(lambda x: strip_end_noise(x))
    df['CLEAN_ADDRESS'] = df['CLEAN_ADDRESS'].apply(lambda x:
                                                    ' '.join(x.split()[:-1])
                                                    if end_has_numbers(x)
                                                    else x)
    df['CLEAN_ADDRESS'] = df['CLEAN_ADDRESS'].apply(lambda x:
                                                    ' '.join(x.split()[:-1])
                                                    if end_is_single_char(x)
                                                    else x)
    df['CLEAN_ADDRESS'] = df['CLEAN_ADDRESS'].apply(lambda x:
                                                    x.replace('PKWY',
                                                              'PARKWAY'))
    df['CLEAN_ADDRESS'] = df['CLEAN_ADDRESS'].apply(lambda x:
                                                    x.replace('AVE RD',
                                                              'AVE'))
    df['CLEAN_ADDRESS'] = df['CLEAN_ADDRESS'].apply(lambda x:
                                                    x.replace('AVE AVE',
                                                              'AVE'))
    df = df.drop_duplicates('ADDRESS').copy()
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


# retrieve API key from config file
key = google_api.google_api_key
# load in raw business
df = pd.read_csv(sys.stdin, low_memory=False)
latlng_df = df[pd.isnull(df['LOCATION'])].copy()
# Remove trialing noise from addresses (i.e., apparment numbers, letters, etc)
latlng_df = add_clean_street_address(latlng_df)

# Set of a clean addresses to send to API for LAT | LNG
clean_addr = set(latlng_df.CLEAN_ADDRESS)

# Make dictionary to store address to lat|lng mapping
addr_to_coordinate_dict = {}
# API call to retrieve lat lng for each clean addr
for addr in clean_addr:
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
        lat, lng = extract_lat_lng(r)
        addr_to_coordinate_dict[addr] = [lat, lng]

# Store LATITUDE and LONGITUDE in dataframe
for k, v in addr_to_coordinate_dict.iteritems():
    latlng_df.loc[latlng_df['CLEAN_ADDRESS'] == k, 'LATITUDE'] = v[0]
    latlng_df.loc[latlng_df['CLEAN_ADDRESS'] == k, 'LONGITUDE'] = v[1]

# Assign Lat| Lng from new df to original df where address columns match
df.loc[df.ADDRESS.isin(latlng_df.ADDRESS),
       ['LATITUDE', 'LONGITUDE']] = latlng_df[['LATITUDE', 'LONGITUDE']]

# SAVE OUTPUT
df.to_csv(sys.stdout, index=False)
