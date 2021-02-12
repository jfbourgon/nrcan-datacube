#!/usr/bin/env python

import argparse

import json
import requests
import shapely.wkt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('collection', metavar='collection', help='collection name')
    parser.add_argument('asset', metavar='asset', help='asset name')
    parser.add_argument('geometry', metavar='geometry', help='input geometry as WKT')
    args = parser.parse_args()

    stac_search = "https://datacube.services.geo.ca/api/search"
    collection_name = args.collection
    asset_name = args.asset
    geometry = args.geometry

    #aoi = shapely.wkt.loads('POLYGON ((-80.81231361783799 51.92168725335885, -80.81231361783799 53.47646421134422, -88.57094093957778 53.47646421134422, -88.57094093957778 51.92168725335885, -80.81231361783799 51.92168725335885))')
    aoi = shapely.wkt.loads(geometry)
          
    payload={
        "intersects": shapely.geometry.mapping(aoi),
        "collections": [
            collection_name
        ]
    }

    response = requests.request("POST", stac_search, data=json.dumps(payload))
    items = json.loads(response.text)

    assert len(items['features']) > 0,"No feature found"

    for item in items['features']:
        print(item['assets'][asset_name]['href'])

if __name__ == "__main__":
    main()