#!/usr/bin/env python

import fiona
import shapely

def main():
    tile_size = 800000
    
    # Load canada.geojson file with fiona
    
    # Create an initial tile polygon with shapely that is adjacent to the projection origin (0, 0)
    # POLYGON ((800000 0, 800000 800000, 0 800000, 0 0, 800000 0))
    
    # Confirm that the proposed tile is located over the canadian landmass (canada.geojson) by performing a spatial intersection with shapely
    
    # Repeat steps 2 & 3 for a new tile adjacent to the previous one
    # POLYGON ((1600000 0, 1600000 800000, 800000 800000, 800000 0, 1600000 0))
    
    # Persist all the computed tiles to an output file using fiona  
    

if __name__ == "__main__":
    main()