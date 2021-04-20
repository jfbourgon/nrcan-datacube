#!/usr/bin/env python
import matplotlib.pyplot as plt
import json
from shapely.geometry import Polygon, shape, box, mapping
import geopandas as gpd
from shapely import wkt
from shapely.geometry import box
from shapely.ops import transform
import pyproj
import argparse

'''
Purpose:
    Explore STAC API + Geopandas inside a Jupyter notebook to compute spatial intersection between STAC collections and use the intersection to make an OGC getmap request.
Example of command:
    C:/Users/Owner/COOP4/PortableGit/nrcan-datacube/all_Python_scripts/module02_intersection.py "https://datacube.services.geo.ca/api/search?collections=salish"
'''


def main():

    # Add argument 
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help="the collection from STAC API", type=str)
    args = parser.parse_args()
    
    # Read the collection from STAC API and create a geoDataFrame based on the geojson
    url = args.url
    gdf = gpd.read_file(url)
    print(gdf)
    
    # Extract all geometries as well as their ids and form a list of geometry
    geom = gdf.geometry
    matrix = []
    # create a list of id and geometry for all the polygons
    for i in range(len(gdf)):
        cur_geom = {'id':[gdf.id[i]], 'geometry':shape(geom[i])}
        cur_gdf = gpd.GeoDataFrame(cur_geom, crs = "EPSG:4326")
        matrix.append(cur_gdf)
    print(matrix)
    
    # Find the intersection of all geometries in the Salish collection
    result=[]
    result.append(gpd.overlay(matrix[0],matrix[1],how='intersection'))
    for i in range (0,len(matrix)-2,1):
        cur = gpd.overlay(result[i],matrix[i+2], how='intersection')
        result.append(cur)
    #take the last result
    final = result[-1]
    print(final)
    
    # Reproject the tilings to the same coordinate system of basemap and convert it into a geodataframe
    bound_box = box(*final.total_bounds)
    project = pyproj.Transformer.from_proj(
        pyproj.Proj('epsg:4326'),
        pyproj.Proj('epsg:32610'),
        always_xy=True) # destination coordinate system

    proj_test = transform(project.transform, bound_box)  # apply projection
    print(proj_test.bounds)
    
    # Use this intersection polygon as bbox and time range to pass a getmap request to the OGC
    
    minx = final.total_bounds[0]
    miny = final.total_bounds[1]
    maxx = final.total_bounds[2]
    maxy = final.total_bounds[3]
    new_bbox = [miny,minx,maxy,maxx]
    start = gdf.datetime[0]
    end = gdf.datetime[len(gdf)-1]
    crs = gdf.crs
    def getUrl(collection='salish',parameter='datacube',value='notset',start_date=start,end_date=end,width='732',height='982'):
        layers='salish'
        crs="EPSG:4326"
        x = ""+ str(miny) + ',' + str(minx) + ',' + str(maxy) + ',' + str(maxx) 
        url = "https://datacube.services.geo.ca/ows/aerial?service=wms&request=GetMap&styles=&format=image/png"
        url+="&LAYERS=%s&WIDTH=%s&HEIGHT=%s&CRS=%s&"%(layers,width,height,crs)

        url+="BBOX=%s"%(x)
        url+="&TIME=%sT12:00:00Z/%sT12:00:00Z"%(start_date,end_date)
        url+="&%s=%s"%(parameter,value)
        return url
    url=getUrl(collection='salish',parameter='datacube',
                           value='notset',start_date=start,
                           end_date=end,width='732',height='982')
    print(url)
    
    

    

if __name__ == "__main__":
    main()