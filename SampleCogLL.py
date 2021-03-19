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
## REFERENCES:
## https://rasterio.readthedocs.io/en/latest/topics/windowed-rw.html
## https://numpy.org/doc/stable/reference/routines.statistics.html
## https://gdal.org/drivers/raster/gtiff.html#georeferencing
## https://rasterio.readthedocs.io/en/latest/topics/plotting.html
## https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html
## https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
##############################
##  TODO:
##  modify so it runs on args passed in as parameters
##  other
###################### selecting portion of cog based on user defined lat/lon window

from shapely.geometry import box, mapping, shape
from rasterio.warp import transform_geom
import rasterio
from datetime import datetime

def main():
    print("start")
    print(datetime.now())
######   Test cases different dem tiles url and appropriate bbox in lon,lat EPSG:4326
##    # define the select window longitude and latitude
####    url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-25-dem.tif"
####    miny=-64.7
####    maxy=-64.8
####    minx=46.5
####    maxx=46.6
####
####    # JF's original coordinates (was not completed after 15 minutes on country internet)
####    url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-11-dem.tif"
####    miny=-63.5
####    maxy=-68.5
####    minx=63.25
####    maxx=68.25
####    # Norah had to use a smaller size (download took aprox 8 minutes on country internet) 
####    miny=-68.5
####    maxy=-66.5
####    minx=66.25
####    maxx=68.25
##    
##    #http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-7-dem.tif
##    miny=-139.5
##    maxy=-137.5
##    minx=60.0
##    maxx=62.0
##    ## open cog by url
##
##    url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-7-dem.tif"
##    file_name="./sample-%s"%(url.split('/')[-1])
##    # open witn all types of GeoTIFF georeference except that within the TIFF file’s keys and tags turned off
##
##    cog=rasterio.open(url,GEOREF_SOURCES='INTERNAL')  
##    #cog bounds and crs
##    print(cog.bounds)
##    print(cog.crs)
##    print(cog.dtypes[0])
##    print(cog.transform)
##    print(cog.nodata)
##    print(cog.shape)
##    print(cog.meta)
##    print(cog.block_shapes)
##    #reproject the window in the cogs projection
##    llbox=box(miny,minx,maxy,maxx)
##    coords_window=shape(transform_geom('EPSG:4326',cog.crs,mapping(llbox)))
##    # select window bounds as var
##    wb=coords_window.bounds
##    print(wb)
##    # create the sample window from the bounds using the cogs (rasterio) window method
##    sample_window=cog.window(wb[0],wb[1],wb[2],wb[3])
##    print(sample_window)
##    # read the sample from the image, 
##    # underlying gdal functionality may resample using nearest neighbour
##    # based on your download speed this could take a while
##    sample_cog=cog.read(1,window=sample_window)
##    print(sample_cog)
##    # write the sample out to a file 'sample_<filename>'
##    with rasterio.open(
##        file_name,
##        'w',
##        driver='GTiff',
##        height=sample_cog.shape[0],
##        width=sample_cog.shape[1],
##        count=1,
##        dtype=cog.dtypes[0],
##        crs=cog.crs,
##        transform=cog.transform,
##        nodata=cog.nodata,
##        GEOREF_SOURCES='INTERNAL'
##    ) as dst:
##        dst.write(sample_cog, 1)
##    dst.close()
##    cog.close()



    ###################### getting histogram statistics using rasterio, matplotlib and numpy
    import rasterio 
    from rasterio.plot import show_hist, show
    from matplotlib import pyplot
    from mpl_toolkits.mplot3d import Axes3D
    import numpy
    # if using all code from above pass file name to sample, if not then define sample
    ##sample=file_name 
    sample='C:\\users\\nbrown\\documents\\datacube\\stage\\example-code\\sample-cdem-7-dem.tif'
    cog_sample=rasterio.open(sample)
    print("bounds: %s"%(str(cog_sample.bounds)))
    print("crs: %s"%(cog_sample.crs))
    print("data type: %s"%(str(cog_sample.dtypes[0])))
    print("transform: %s"%str((cog_sample.transform)))
    print("pixel resolution from transform: %s"%(str(cog_sample.transform[0])))
    print("no data: %s"%(str(cog_sample.nodata)))
    print("image size in pixes: %s" %(str(cog_sample.shape)))
    print("cog header info: %s"%(cog_sample.meta))
    
    #make a figure with two axes subplot
    fig, (aximage, axhist) = pyplot.subplots(1, 2, figsize=(7,4))
    figtitle="original sample cog and histogram"
    fig.suptitle(figtitle,fontsize=10)

    #create histogram using rasterio show histogram, pass axes subplot handle to axhist
    bins=50
    show_hist(cog_sample, bins=bins, lw=0.0, 
              stacked=False, alpha=0.3,
              histtype='stepfilled',
              ax=axhist)
    axhist.set_title('')
    axhist.set_xlabel('elevation (m)')
    axhist.set_ylabel('')
    axhist.legend('')
    #create display image passing axes subplot handle to aximage
    show(cog_sample, cmap='gray',transform=cog_sample.transform, ax=aximage)
    #save the figure
    fname='./im-hist-test.png'
    pyplot.savefig(fname,format='png')
    #plot the figure
##    pyplot.show()

######### 3D plots start
##    # create a 3d axes
##    fig = pyplot.figure()
##    ax = fig.add_subplot(111, projection='3d')
##    #create a 1D array for x /columns / longitude
##    x=numpy.arange(cog_ar.shape[1])
##    #create a 1D array for y/ rows / lattitude
##    y=numpy.arange(cog_ar.shape[0])
##    # merge two 1D arrays in a 2d xy array
##    X,Y=numpy.meshgrid(x,y)
##    # replace no data value with 'not a number'
##    # could also try empty
##    cog_ar=numpy.where(cog_ar<-32766,numpy.nan,cog_ar)
##    cog_ar=numpy.where(cog_ar<-32766,numpy.nan,cog_ar)
##    ax.plot_wireframe(X,Y,cog_ar)
##    ax.plot_surface(X,Y,cog_ar)
##    # plot the 3d surface
##    pyplot.show()
########  3D plots end

                   
    #get stats from array  
    cog_sample=rasterio.open(sample)
    #read cog into numpy array
    cog_ar=cog_sample.read(1)
    #min
    print(numpy.amin(cog_ar))
    #max
    print(numpy.amax(cog_ar))
    # plot the image
    #pyplot.show()
    #close image read
    cog_sample.close()
    print("finished")
    print(datetime.now())
if __name__ == '__main__':
    main()



########## APPENDIX of code for interest

####### Range Request
##### hacked from
####    https://requests.readthedocs.io/en/master/user/quickstart/
####    https://zetcode.com/python/urllib3/
####    https://docs.python.org/3/library/io.html#in-memory-streamsS
##from datetime import datetime
##import requests
##import urllib3
##import certifi
##import io
##print("start")
##print(datetime.now())
#####check if resource accepts range requests
##url="http://datacube-prod-data-public.s3.ca-central-1.amazonaws.com/store/dem/cdem/cdem-11-dem.tif"
##h=requests.head(url)
##hs=h.headers
##print(hs['Accept-Ranges']) #returns 'bytes' if range requests accepted
###attach ssl certificate
##http = urllib3.PoolManager(ca_certs=certifi.where())
###set up byte range
##byte_min=0
##byte_max=45000
##chunks=1024#256
##current_min=0
##current_max=chunks
##print("min: %s, max: %s, chunk: %s"%(current_min,current_max,chunks))
###define get parameters
##params=""
##f=io.open("test.tif",'ab')
### Loop through requesting different byte ranges
### until hit final byte range
##while (byte_max>current_max):
##    #define get headers
##    headers={"Range": "bytes=%s-%s"%(current_min,current_max)}
##    #get response from request
##    resp = http.request('GET', url,params,headers)
##    #write byte stream to file
##    f.write(resp.data)
##    current_min=current_min+chunks+1
##    current_max=current_max+chunks+1
##    #print("min: %s, max: %s, chunk: %s"%(current_min,current_max,chunks))
##    #print(resp.status, resp.reason) # 206 Partial Content
##    resp.close()
##print("out of while")
##print("min: %s, byte_max: %s"%(current_min+1,byte_max))
##headers={"Range": "bytes=%s-%s"%(current_min+1,byte_max)}
##resp = http.request('GET', url,params,headers)
##print(resp.status, resp.reason) # 206 Partial Content
##f.write(resp.data)
##f.close()
##resp.close()
##print("final stream of data")
##print(resp.data)
##print("end")
##print(datetime.now())
### Dont forget to deal with header in the cog
### Using rasterio window is simpler
