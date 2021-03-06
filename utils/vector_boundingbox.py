#!/usr/bin/env python

import argparse

import json
import fiona
import pyproj
import shapely
from shapely.geometry import shape, box
from shapely.ops import transform


def get_feature(ds, fid):
    # read only the selected feature from the dataset
    f = ds[fid]
    assert f != None,"Feature not found"
    return f

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--format', default='wkt', help='output format')
    parser.add_argument('--fid', type=int, default=0, help='feature id')
    parser.add_argument('--latlong', default=False, action='store_true', help='reproject to Lat/Long coordinates (WGS84)')
    parser.add_argument('input', metavar='input', help='path to dataset')
    args = parser.parse_args()
    
    input = args.input
    fid = args.fid
    format = args.format

    # open the input dataset in read mode
    ds = fiona.open(input)

    f = get_feature(ds, fid)

    # convert bounds to Polygon
    bounds = shape(f['geometry']).bounds
    geom = box(*bounds)

    if (args.latlong):
        projection = pyproj.Transformer.from_crs(ds.crs['init'], pyproj.CRS('EPSG:4326'), always_xy=True).transform
        projected = transform(projection, geom) 
        geom = projected

            
    print("BBOX:")
    print(geom.bounds)
    
    print("Envelop:")
    if format.lower() == 'geojson':
        geojson = shapely.geometry.mapping(geom)
        print(json.dumps(geojson))
    else:
        print(geom.wkt)

if __name__ == "__main__":
    main()










































































































































































































































































































































































