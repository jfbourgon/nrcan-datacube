#!/usr/bin/env python

import fiona
import fiona.crs
from shapely.geometry import Polygon, shape, box, mapping
import math

import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('size', metavar='size', type=int, help='tile size')
    parser.add_argument('output', metavar='output', help='output filename')
    args = parser.parse_args()

    tile_size = args.size
    output = args.output
    
    # Load canada.geojson file with fiona
    source = fiona.open('./canada.geojson')
    canada = shape(source[0]["geometry"])
    
    container = []
    
    # Set ranges from canada extent and suggested tile size
    range_minx = math.floor(source.bounds[0]/tile_size)
    range_maxx = math.ceil(source.bounds[2]/tile_size)
    range_miny = math.floor(source.bounds[1]/tile_size)
    range_maxy = math.ceil(source.bounds[3]/tile_size)
    
    for i in range(range_minx,range_maxx):
        x = i * tile_size
        for j in range(range_miny,range_maxy):
            y = j * tile_size
            # Create tile polygon with shapely 
            my_tile = box(x, y , x + tile_size, y + tile_size)
            # Confirm that the proposed tile is located over the canadian landmass by performing a spatial intersection with shapely
            if my_tile.intersects(canada):
                container.append(my_tile)

    # Persist all the computed tiles to an output file using fiona 
    schema = {
        'geometry': 'Polygon',
        'properties': {'id': 'int'},
    }
    
    with fiona.open(output,'w','GeoJSON',schema, crs=fiona.crs.from_epsg(3979)) as filename:
        for i in container:
            index = 0
            filename.write({
                'geometry': mapping(i),
                'properties': {'id': index+1}
            })

if __name__ == "__main__":
    main()