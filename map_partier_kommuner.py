# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing for which municipalities a given party is largest."""
import json
import pathlib
import sys
import pandas as pd
from map_basics import produce_map


# Define paths to the raw geojson files:
KOMMUNE_DIR = pathlib.Path('kommuner')
KOMMUNE_KRETS = 'kommune-{}.geojson'


def get_geojson_data(result_files):
    """Read in result files and produce corresponding geojson data."""
    all_geojson_data = []
    for result_file in result_files:
        print('Reading file:', result_file)
        new_data = {'features': []}
        results = pd.read_json(result_file)
        kommuner = results['Kommunenummer'].tolist()
        # The input data is assumed to be structured so that it only
        # contains data for one party:
        parti = results['Partinavn'].tolist()[0]
        for kommune in kommuner:
            kommune_id = '{}'.format(kommune).rjust(4, '0')
            geojson_file = KOMMUNE_DIR.joinpath(
                KOMMUNE_KRETS.format(kommune_id)
            )
            print('Loading:', geojson_file)
            with open(geojson_file, 'r') as infile:
                geojson_data = json.load(infile)
            for key in ('crs', 'type'):
                if key not in new_data:
                    new_data[key] = geojson_data[key]
            for feature in geojson_data['features']:
                feature['properties']['partinavn'] = parti
                new_data['features'].append(feature)
        if new_data['features']:
            all_geojson_data.append((parti, new_data))
    return all_geojson_data


def main(result_files):
    """Read input files and create the map."""
    geojson_layers = get_geojson_data(result_files)
    if len(result_files) == 1:
        filename = pathlib.Path(result_files[0]).stem
        out = '{}.html'.format(filename)
    else:
        out = 'map-partier-kommuner.html'
    produce_map(geojson_layers, [63., 10.], 10, output=out)


if __name__ == '__main__':
    main(sys.argv[1:])
