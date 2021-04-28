#!/usr/bin/env python

import rasterio 
import matplotlib.pyplot as plt
from rasterio.plot import show_hist, show
from matplotlib import pyplot
import numpy
import os
import sys
import glob
import csv
import pandas as pd
import argparse

'''
Purpose: 
Create overviews using different resampling methods and export the thumbnails / histograms / statistics of each image
    
Example of command:
C:/Users/Owner/COOP4/PortableGit/nrcan-datacube/all_Python_scripts/module03_resample.py C:/Users/Owner/COOP4/PortableGit/nrcan-datacube/all_Python_scripts/test1/dem-source_22.tif 64   
'''

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source_dem', metavar='source_dem', type=str, help='source_dem path')
    parser.add_argument('factor', metavar='factor', type=int, help='dec factor')
    args = parser.parse_args()
    source_dem = args.source_dem
    factor = args.factor

    dem = source_dem.split('/')[-1]
    path = source_dem.replace(dem,'')
    output_path = path + '{}_{}.tif' 

    # Resample the source image using different resampling methods
    resample_list = ['nearest','average','bilinear','gauss','cubic','cubicspline','average_magphase','mode']
    dec_factor = str(factor)

    for resample in resample_list:
        print("gdaladdo -r "+ resample +" -ro " + source_dem + " --config COMPRESS_OVERVIEW LZW " + dec_factor)
        os.system("gdaladdo -r "+ resample +" -ro " + source_dem + " --config COMPRESS_OVERVIEW LZW " + dec_factor)
        ovr = '.ovr'
        ovr_path = r'{}{}'.format(source_dem,ovr) 
        new_path = output_path.format(resample,dec_factor)
        os.rename(ovr_path,new_path)
    # Pass the information / metadata from the source image to the overviews
    cog = rasterio.open(source_dem)
    sample_cog = cog.read(1)
    dec = factor
    
    for i in resample_list:
        path = output_path.format(i,str(factor))
        arr = rasterio.open(path)
        dtype = arr.dtypes[0]
        array = arr.read(1)
        arr.close()
        
        with rasterio.open(
            path,
            'w+',
            driver='GTiff',
            height=sample_cog.shape[0]//dec,
            width=sample_cog.shape[1]//dec,
            count=1,
            dtype=dtype,
            crs=cog.crs,
            transform=cog.transform,
            nodata=cog.nodata,
            GEOREF_SOURCES='INTERNAL') as dst:
            dst.write(array, 1)
            dst.close()
            cog.close()
    
    
    # Read each resampled image an then:
    #  extract the information
    #  create a thumbnail and histogram
    for filename in glob.glob(os.path.join(path, '*.tif')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            cog_sample = rasterio.open(filename)
            cur_name = os.path.basename(filename)[:-4]
    
            bound = str(cog_sample.bounds)
            crs = str(cog_sample.crs)
            dtype = str(cog_sample.dtypes[0])
            trans = str(cog_sample.transform)
            nodata = str(cog_sample.nodata)
            shape = str(cog_sample.shape)
            meta = str(cog_sample.meta)
            output = "{}_info".format(cur_name)
            f = open(output+'.txt',"w")
            f.write("stats: " + "\n" + 
                    "bound: " + bound + "\n" + 
                    "crs: " + crs + "\n" + 
                    "dtype: " + dtype + 
                    "transform: " + trans + 
                    "nodata: " + nodata + 
                    "shape: " + shape + 
                    "metadata: " + meta)
    
            fig, (aximage, axhist) = pyplot.subplots(1, 2, figsize=(49,28))
            figtitle="{} sample cog and histogram".format(cur_name)
            fig.suptitle(figtitle,fontsize=30)
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
            fname=path+cur_name+'.png'
            pyplot.savefig(fname,format='png')

    fields = ['Name', 'Resampling_Method', 'Overview', 'Driver', 'Data Type', 
          'crs', 'Width', 'Height', 'Nodata_Pixels', 'Pixels_with_Values',
          'Pixel_Size', 'Min', 'Max', 'Range', 'Q1', 'Q3', 'Mean', 'Median', 
          'Std', 'Var']
    rows = [fields]
    for filename in glob.glob(os.path.join(path, '*.tif')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f: # open in readonly mode
            cog = rasterio.open(filename)
            cur_name = os.path.basename(filename).split('_')[0]
            resampling = os.path.basename(filename)[:-7]
            overview = 32

            # delete nodata value
            cog_ar = cog.read(1)
            cog_ar = numpy.where(cog_ar==cog.nodata,numpy.nan,cog_ar)
    
            # stats
            driver = str(cog.meta['driver'])
            dtype = str(cog.meta['dtype'])
            crs = str(cog.meta['crs'])
            width = cog.meta['width']
            height = cog.meta['height']
            nodata = len(cog_ar[numpy.isnan(cog_ar)])
            data_with_values = len(cog_ar[~numpy.isnan(cog_ar)])
            pixel_size = cog.transform[0]
            
            cog_min = numpy.nanmin(cog_ar)
            cog_max = numpy.nanmax(cog_ar)
            cog_range = cog_max-cog_min
            cog_q1 = numpy.nanquantile(cog_ar, 0.25)
            cog_q3 = numpy.nanquantile(cog_ar, 0.75)
            cog_mean = numpy.nanmean(cog_ar)
            cog_median = numpy.nanmedian(cog_ar)
            cog_std = numpy.nanstd(cog_ar)
            cog_var = numpy.nanvar(cog_ar)
    
            cur_row = [cur_name,
                    resampling,
                    overview,
                    driver,
                    dtype,
                    crs,
                    width,
                    height,
                    nodata,
                    data_with_values,
                    pixel_size,
                    cog_min,
                    cog_max,
                    cog_range,
                    cog_q1,
                    cog_q3,
                    cog_mean,
                    cog_median,
                    cog_std,
                    cog_var]
            
            rows.append(cur_row)
            # name of csv file
            opath = path+'stats_{}.csv'
            output = opath.format(cur_name)
            
            # writing to csv file 
            with open(output, 'w',newline='') as csvfile: 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerow(fields) 
                csvwriter.writerow(cur_row)
                
    # name of csv file
    output = "{}/stats_all.csv".format(path)

    # writing to csv file 
    with open(output, 'w',newline='') as csvfile: 
        csvwriter = csv.writer(csvfile) 
        csvwriter.writerows(rows)

if __name__ == "__main__":
    main()