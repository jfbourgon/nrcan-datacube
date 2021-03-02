#!/usr/bin/env python
import geopandas as gpd
import argparse
import pathlib
import os

def main():
    # import files
    parser = argparse.ArgumentParser()
    parser.add_argument('tiledf', metavar='input', help='path to tiler_polygons')
    parser.add_argument('coveragedf', metavar='input', help='path to coverage')
    parser.add_argument('outputpath',type=pathlib.Path)
    
    args = parser.parse_args()
    
    tiledf = args.tiledf
    coveragedf = args.coveragedf
    outputpath = args.outputpath
    
    gpd_tiledf = gpd.read_file(tiledf)
    gpd_coveragedf = gpd.read_file(coveragedf)
    
    '''
    len(tiledf)
    len(coveragedf)
    print(tiledf)  
    print(coveragedf)
    '''
    
    # create and visualize tiler intersection
    tile_intersection = gpd.overlay(gpd_coveragedf,gpd_tiledf, how='intersection')
    
    '''
    ax = tile_intersection.plot(color='aqua')
    coveragedf.plot(ax=ax, facecolor='none', edgecolor='k');
    tiledf.plot(ax=ax, facecolor='none', edgecolor='k');
    '''
    
    for key, groupdf in tile_intersection[['id', 'NTS_SNRC']].groupby('id'):
        if not os.path.exists(outputpath):
            os.mkdir(outputpath)
            print("Directory " , outputpath,  " Created ")
        groupdf['NTS_SNRC'].to_csv(os.path.join(outputpath,"{}.txt".format(key)), header = False, index=False)

if __name__ == "__main__":
    main()