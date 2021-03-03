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
## Python Map projections
* based on module 2
* experiment with plotting different standard ipyleaflet projections (https://ipyleaflet.readthedocs.io/en/latest/api_reference/map.html)
* experiment with plotting custom ipyleaflet projections (https://github.com/jupyter-widgets/ipyleaflet/issues/612)  (http://epsg.io/)
* experiment with plotting projections using matplotlib (https://matplotlib.org/3.2.1/gallery/subplots_axes_and_figures/geo_demo.html)
