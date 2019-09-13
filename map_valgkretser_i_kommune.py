# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing the largest party in different voting areas."""
import pathlib
import sys
import pandas as pd
import numpy as np
from map_basics import produce_map, load_json_file


VALGKRETS_DIR = pathlib.Path('valgkretser')
VALGKRETS = 'krets-{}.geojson'


def _add_coordinates(feature, coordinates):
    """Add coordinates from a feature."""
    coords = []
    for polygon in feature['geometry']['coordinates']:
        for row in polygon:
            coords.append(row)
    coordinates.append(np.average(coords, axis=0))


def get_geojson_data(result_files):
    """Read in result files are produce corresponding geojson data."""
    all_geojson_data = []
    coordinates = []
    for result_file in result_files:
        print('Reading file "{}"'.format(result_file))
        results = pd.read_json(result_file)
        # Each file contains the result for a single municipality:
        kommune = results['Kommunenummer'].tolist()[0]
        kommune_navn = results['Kommunenavn'].tolist()[0]
        # Check if we do actually have several voting areas or just
        # one for the whole municipality:
        use_all = results['Stemmekretsnavn'].tolist()[0] == 'Hele kommunen'
        geojson_file = VALGKRETS_DIR.joinpath(
            VALGKRETS.format(
                str(kommune).rjust(4, '0')
            )
        )
        geojson_data = load_json_file(geojson_file)
        parti = results[results['Kommunenummer'] == kommune]['Partinavn']
        for feature in geojson_data['features']:
            if not use_all:
                # Update to new region:
                nummer = feature['properties']['valgkretsnummer']
                parti = results[
                    results['Stemmekretsnummer'] == nummer
                ]['Partinavn']
            feature['properties']['partinavn'] = parti.tolist()[0]
            _add_coordinates(feature, coordinates)
        all_geojson_data.append((kommune_navn, geojson_data))
    avg = np.average(coordinates, axis=0)
    return all_geojson_data, avg


def main(result_files):
    """Read input files and create the map."""
    geojson_data, center = get_geojson_data(result_files)
    if len(result_files) == 1:
        filename = pathlib.Path(result_files[0]).stem
        out = 'valgkretser-{}.html'.format(filename)
    else:
        out = 'map-valgkretser.html'
    produce_map(geojson_data, center[::-1], 10, output=out)


if __name__ == '__main__':
    main(sys.argv[1:])
