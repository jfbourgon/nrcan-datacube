# Module 2
## STAC Data Frames in a Jupyter Notebook
Explore STAC API + Geopandas inside a Jupyter notebook to compute spatial intersection between STAC collections and use the intersection to make an OGC getmap request  
 > * The NAPL STAC collections have overlaps between time periods of the same collection
 > * The Salish collection has the most time periods and should be used is this module.
 > * Each item in the Salish collection has different temporal and geographic extents
 > * The OGC WMS accepts a get map request based on the available layers, bbox and time(datetime) (https://datacube.services.geo.ca/ows/aerial?service=wms&request=GetCapabilities)

## Work to be done
1. Using the STAC API create geopanda dataframes for each item (feature) in the Salish collection (https://datacube.services.geo.ca/api/search?collections=salish)
1. Generate an intersection polygon with an extent that is shared by all the temporal items
      > save this information with additional attributes (temporal data, other) in an appropriate format (geojson, csv, other) and appropriate coordiante reference system (crs)
1. Use this intersection polygon as  bbox and time range to pass a getmap request to the OGC WMS server parameters include:
    * bbox : polygon extent
    * time : the datatime range
    * crs : an acceptable coordinage reference system that is listed in the getcapabilities and matches the coordinates of the bbox
    * example link (https://datacube.services.geo.ca/ows/aerial?service=wms&request=GetMap&styles=&format=image/jpeg&layers=salish&version=1.3&height=732&width=982&bbox=-122.4,49.1,-122.2,49.2&crs=EPSG:4326&TIME=1950-01-01T00:00:00Z/1982-01-01T00:00:00Z&transparent=true)
1. (Optional) Use this intersection polygon as a clip shape to extract a portion of the cog image using rasterio





If there is time, intersections between NAPL and DEM collections can be attempted
## National Air Photo Library (NAPL) temporal mosaic collection
### Salish temporal mosaics 6 time periods
(https://datacube.services.geo.ca/api/collections/salish/)
### Halifax temporal mosaics 2 time periods
(https://datacube.services.geo.ca/api/collections/halifax/)
### Markham temporal mosaics 2 time periods
(https://datacube.services.geo.ca/api/collections/markham/)

## DEM collections
### Canadian Digital Elevation Model (CDEM) mosaics 
(https://datacube.services.geo.ca/api/collections/cdem/)
### Canadian Digital Surface Model (CDSM) mosaics
(https://datacube.services.geo.ca/api/collections/cdsm/)

## Introduction to clipping rasters with vectors:
(https://automating-gis-processes.github.io/CSC/notebooks/L5/clipping-raster.html)
