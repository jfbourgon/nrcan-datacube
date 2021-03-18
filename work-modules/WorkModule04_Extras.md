# Extra Work Modules
## Enhanced metadata using STAC extensions
* review extension options from eo and datacube
    * https://github.com/radiantearth/stac-spec/blob/master/best-practices.md
    * https://github.com/radiantearth/stac-spec/tree/v0.6.2/extensions/datacube
* develop decision matrix on optional extensions and which image types they should apply to
* create add-to-stac.py to include new extensions to existing stacs
* modify create-stac.py to include new extensions
* test validation of stac files using pystac
## Single band vs multi band cogs – experimentation using python or r, 
* test accessing single band images, 
* generate multiband image, 
* generate basic band statistics, 
* document file size, other storage and dissemination pros, cons, concerns.
## Dissemination Database (MySQL database or Maria database)
Query optimisation 
* Generation of geospatial data (bbox / or study area polyogon)
* Geospatial statistics on study areas using qgis and tables or extracts
* User needs Data modeling and report generation for operational monitoring or business reporting
* Franklin s3 compare (franklin component)
## Python, Leaflet, Qgis wms test clients
* develop availability metrics request type / response time / time outs etc
* develop test cases
* develop automated tests using python –urlib, urlib2, urlib2,httplib, or requests module, make recommendations on modules to use
* develop manual test and leaflet client
* develop manual test in qgis
* test gt – wms vs mapserver wms
## Different methods to stream a portion of a cog
* test difference in download time and difference in data sampling between
* rasterio read with user defined window 
    ```
    llbox=box(miny,minx,maxy,maxx)
    coords_window=shape(transform_geom('EPSG:4326',cog.crs,mapping(llbox)))
    wb=coords_window.bounds
    sample_window=cog.window(wb[0],wb[1],wb[2],wb[3])
    sample_cog=cog.read(1,window=sample_window)
    ```
* rasterio read with image defined window blocks
https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html#blocks
* gdal 
    ```
    gdalwarp --config CPL_VSIL_CURL_ALLOWED_EXTENSIONS ".tif" -t_srs epsg:3979 -te_srs epsg:4326 -te -68.5 68.25 -63.5 63.25 -tr 16 16 -ovr NONE -tap /vsicurl/http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-11-dem.tif dem-source.tif
    ```
* http get range request
    ```
    headers={"Range": "bytes=%s-%s"%(current_min+1,byte_max)}
    resp = http.request('GET', url,params,headers)
    print(resp.status, resp.reason)
    print(resp.data)
    ```

## Athematic to thematic overview creation
* Use athematic data to create themed / classified data
* test difference between overviews created from thematic layer vs overviews created from same level overview of athematic data
## Rasterio Window Utilities Test
https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html#window-utilities
https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html#blocks
* test accessing windows with and without aligning to internal block_size
* test generating statistics on select area of base imagery and overviews
