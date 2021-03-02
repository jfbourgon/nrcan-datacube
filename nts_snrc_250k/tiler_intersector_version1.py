#!/usr/bin/env python
import fiona
import fiona.crs
import shapely
from shapely.geometry import Polygon, shape, box, mapping
import geopandas as gpd
import argparse

def main():
    # Read proposed tiling (output of your first script)
    tiles = fiona.open('nts_snrc_250k/output.geojson')
    # Read existing coverage (attached file)
    coverage = fiona.open('nts_snrc_250k/nts_snrc_250k.geojson')

    # Create dataframe of nts_snrc_250k.geojson
    df_coverage = []
    for i in range(1,len(coverage)):
        cov = shape(coverage[i]['geometry'])
        df_coverage.append(cov)
   
    # Create dataframe of output.geojson
    df_tiles = []

    for i in range(1,len(tiles)+1):
        tile = shape(tiles[i]['geometry'])
        df_tiles.append(tile) 
    
    '''
    # geojson dataframe -> geopandas GeoDataFrame
    tile_geom = [shape(i) for i in df_tiles]
    tile_gdf = gpd.GeoDataFrame({'geometry':tile_geom})
    coverage_gdf = gpd.GeoDataFrame({'geometry':[shape(j) for j in df_coverage]})

    # intersection
    tile_intersection = gpd.overlay(coverage_gdf,tile_gdf, how='intersection')
    # output intersection
    tile_intersection.to_file('nts_snrc_250k/export/intersection.geojson', driver="GeoJSON")
    '''

    # create list of id list
    def poly_with_ids (n):
        gen_list = []
        for j in df_coverage:
            poly1 = []
            if j.intersects(df_tiles[n]):
                cur_index = coverage[df_coverage.index(j)]['properties']['NTS_SNRC']
                poly1.append(cur_index)
                gen_list += poly1
        return (gen_list)

    id_lst=[]
    for n in range(len(df_tiles)):
        lst = poly_with_ids (n)
        id_lst.append(lst)

    # export to text files
    for i,lst in enumerate(id_lst):
        f = open("tile"+str(i+1)+".txt","w")
        for item in lst:
            f.write(item+"\n")
        f.close()

if __name__ == "__main__":
    main()