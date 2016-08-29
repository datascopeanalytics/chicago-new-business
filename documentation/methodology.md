# Methodology

## Data Sources:

From Open Data Portal - City of Chicago:
[business license data ](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr)
[neighborhood boundaries](https://data.cityofchicago.org/download/9wp7-iasj/application/zip)

## Data Prep

Add missing Lat/Lng Data by mapping business addresses using [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/get-api-key)

Map businesses to neighborhood shapefiles filtering out businesses with PO Box addresses and outside Chicago, IL.

Identify new businesses by finding earliest appearance of a business license at a particular location ('ACCOUNT NUMBER' & 'SITE NUMBER') with 'ISSUE' application type.

Identify old businesses by finding latest end date ('LICENSE TERM EXPIRATION DATE') for a particular location ('ACCOUNT NUMBER' & 'SITE NUMBER').

Aggregate counts of new and old businesses by year. To find counts of businesses that continued to operate, cycle through all old businesses and check if issuance for that location is recorded in data. If found, add to number of existing businesses in neighborhood for all years in between issue and expiry years. If not found, set to 2003 (i.e., oldest valid date in dataset). This allows for inclusion of businesses that were established before Data Portal started recording business license data.

## Data Visualization

Using counts of new, old, and continued businesses per neighborhood, percentage change was calculated against 2006 numbers. This year was chosen to represent state of Chicago businesses prior to Great Recession. Cut off year was 2015 as 2016 is still in progress and numbers are incomplete for the year.

The number of businesses (per neighborhood) in a given year is calculated by adding new businesses to continued businesses minus expiring (i.e., old) businesses.

Visualization shows percentage change of the number of businesses relative to 2006 by neighborhood for selected year. Slider is for changing year.

Stats for a particular neighborhood can be seen on hovering over it on map. Number in middle of viz, shows aggregate number across all Chicago; if a neighborhood is selected (by click), this number adjusted to show that neighborhood's stat. If user keeps clicking, multiple neighborhoods are selected and the aggregate number also adjusts to only these neighborhoods. To reset to all of Chicago, click outside map.

Line bar chart, displays the number of new and old businesses across selected neighborhood(s). Line shows the difference and reveals the trend over all years included in the visualization.
