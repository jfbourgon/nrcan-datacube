#!/usr/bin/python3
##############################
## DEV_INFO:
######  Developed by:
##  Norah Brown - Natural Resources Canada, Siyu Li - University of Waterloo, Jean-François Bourgon - Natural Resources Canada
##  Crown Copyright as described in section 12 of Copyright Act (R.S.C., 1985, c. C-42)
##  © Her Majesty the Queen in Right of Canada, as represented by the Minister of Natural Resources Canada, 2019
## FILE_NAME: SampleCogLL.py
##  Python 3.8 (v64b)
##  version 0.0 - 2021/03 nb/sl: initial development 
##  version 0.1 -
##############################
## DESCRIPTION:
##  Selects a subset of cog based on lat lon window, writes it to local file, generates histogram
## USAGE:
##    Currently set up to run on local computer
##    See test case usage for details
##############################
##  TODO:
##  modify so it runs on args passed in as parameters
##  other
###################### selecting portion of cog based on user defined lat/lon window
from shapely.geometry import box, mapping, shape
from rasterio.warp import transform_geom
import rasterio
from datetime import datetime
print("start")
print(datetime.now())
# define the select window longitude and latitude
#url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-25-dem.tif"
#miny=-64.7
#maxy=-64.8
#minx=46.5
#maxx=46.6

#JF's original coordinates (was not completed after 15 minutes on country internet)
#url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-11-dem.tif"
#miny=-63.5
#maxy=-68.5
#minx=63.25
#maxx=68.25
#Norah had to use a smaller size (download took aprox 8 minutes on country internet) 
##miny=-68.5
##maxy=-66.5
##minx=66.25
##maxx=68.25
##http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-7-dem.tif
miny=-139.5
maxy=-137.5
minx=60.0
maxx=62.0
## open cog by url

url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-7-dem.tif"
file_name="./sample-%s"%(url.split('/')[-1])
cog=rasterio.open(url)
#cog bounds and crs
print(cog.bounds)
print(cog.crs)
print(cog.dtypes[0])
print(cog.transform)
print(cog.nodata)
print(cog.shape)
print(cog.meta)
#reproject the window in the cogs projection
llbox=box(miny,minx,maxy,maxx)
coords_window=shape(transform_geom('EPSG:4326',cog.crs,mapping(llbox)))
# select window bounds as var
wb=coords_window.bounds
print(wb)
# create the sample window from the bounds using the cogs (rasterio) window method
sample_window=cog.window(wb[0],wb[1],wb[2],wb[3])
print(sample_window)
# read the sample from the image, 
# underlying gdal functionality may resample using nearest neighbour
# based on your download speed this could take a while
sample_cog=cog.read(1,window=sample_window)
print(sample_cog)
# write the sample out to a file 'sample_<filename>'
with rasterio.open(
    file_name,
    'w',
    driver='GTiff',
    height=sample_cog.shape[0],
    width=sample_cog.shape[1],
    count=1,
    dtype=cog.dtypes[0],
    crs=cog.crs,
    transform=cog.transform,
    nodata=cog.nodata
) as dst:
    dst.write(sample_cog, 1)
dst.close()
cog.close()
print("finished")
print(datetime.now())


###################### getting histogram statistics using rasterio, matplotlib and numpy
### hacked from:
##    https://rasterio.readthedocs.io/en/latest/topics/plotting.html
import rasterio 
from rasterio.plot import show_hist
sample=file_name
cog_sample=rasterio.open(sample)
print(cog_sample.bounds)
print(cog_sample.crs)
print(cog_sample.dtypes[0])
print(cog_sample.crs)
print(cog_sample.transform)
print(cog_sample.nodata)
print(cog_sample.shape)
print(cog_sample.meta)
# view dimensions of image
print(cog_sample.shape)
#put histogram
show_hist(cog_sample, bins=50, lw=0.0, stacked=False, alpha=0.3,histtype='stepfilled', title="Original sample Histogram")
cog_sample.close()

########## APPENDIX of code for interest

####### Range Request
##### hacked from
####    https://requests.readthedocs.io/en/master/user/quickstart/
####    https://zetcode.com/python/urllib3/
##import requests
##import urllib3
##import certifi
#####check if resource accepts range requests
##url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-11-dem.tif"
##h=requests.head(url)
##hs=h.headers
##print(hs['Accept-Ranges']) #returns 'bytes' if range requests accepted
###define get parameters
##params=""
###define get headers
##headers={"Range": "bytes=300-550"}
###attach ssl certificate
##http = urllib3.PoolManager(ca_certs=certifi.where())
###get response from request
##resp = http.request('GET', url,params,headers)
##print(resp.status, resp.reason) # 206 Partial Content
##print(resp.data)
### Loop through requesting different byte ranges
### until hit final byte range
### Dont forget to skip header in the cog
### Using rasterio window is simpler
