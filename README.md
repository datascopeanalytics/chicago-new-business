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
