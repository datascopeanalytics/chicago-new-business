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

3. Run the data analysis pipeline using [flo]()
   ```sh
   flo run
   ```

4. Enjoy the static figures.
   ```sh
   open data/*.png
   ```

5. View the site.
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
   topojson -o neighborhoods.topojson --id-property SEC_NEIGH -p PRI_NEIGH  -- neighborhoods.json
   # Merge polygons for neighborhoods in the same SEC_NEIGH
   topojson-merge -o merged_neighborhoods.topojson --in-object=neighborhoods --out-object=merged_neighborhoods  -- 'neighborhoods.topojson'
   ```
