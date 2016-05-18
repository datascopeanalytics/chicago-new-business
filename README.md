# chicago-new-business
Visualize where new businesses are created in the city

* [business license data ](https://data.cityofchicago.org/Community-Economic-Development/Business-Licenses/r5kz-chrr)

## quickstart

1. Create a python virtualenv with virtualenvwrapper
   ```sh
   mkvirtualenv chicago-new-business
   workon chicago-new-business
   ```

2. Install python dependencies
   ```sh
   pip install -r requirements/python
   ```

3. Sign up for Google Maps Geocoding API and [get key](https://developers.google.com/maps/documentation/geocoding/get-api-key). Store key in src/google_api.py as below
   ```sh
   google_api_key = "YOUR_API_KEY"
   ```

4. Run the data analysis pipeline using [flo]()
   ```sh
   flo run
   ```

5. Enjoy the static figures.
   ```sh
   open data/*.png
   ```

6. View the site.
   ```sh
   cd web && python -m SimpleHTTPServer
   # open http://localhost:8000 in your browser
   ```

## appendix

###### To convert shapefiles into TopoJSONs used in viz:

1. [Install topojson](https://github.com/mbostock/topojson/wiki/Installation) command-line application.

2. Run following commands in /data/boundaries directory.

   ```sh
   # The -t_srs crs:84 specifies a projection to use. If you leave this part off, you won't be dealing with degrees in your output document.
   ogr2ogr -f "GeoJSON" -t_srs crs:84 neighborhoods.json Neighborhoods_2012b.shp
   # Convert to TOPOJSON; specify ID and retain property with -p
   topojson -o neighborhoods.topojson --id-property PRI_NEIGH -p SEC_NEIGH  -- neighborhoods.json
   ```
