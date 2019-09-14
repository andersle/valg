# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing the largest party in different voting areas."""
import pathlib
import sys
import numpy as np
from map_basics import (
    produce_map,
    load_json_file,
    create_tool_tip,
    read_csv_results,
)


VALGKRETS_DIR = pathlib.Path('valgkretser')
VALGKRETS = 'krets-{}.geojson'


def _add_coordinates(feature, coordinates):
    """Add coordinates from a feature."""
    coords = []
    for polygon in feature['geometry']['coordinates']:
        for row in polygon:
            coords.append(row)
    coordinates.append(np.average(coords, axis=0))


def extract_data(results, kommune):
    """Extract the data we want from the results."""
    kommune_data = results[results['Kommunenummer'] == kommune].groupby(
        ['Stemmekretsnummer']
    )
    area = {}
    kretser = []
    for name, group in kommune_data:
        idx = group['Oppslutning prosentvis'].idxmax()
        maxi = results.iloc[idx, :]
        area[name] = {
            'partinavn': maxi['Partinavn'],
            'oppslutning': maxi['Oppslutning prosentvis'],
            'krets': maxi['Stemmekretsnavn'],
        }
        kretser.append(maxi['Stemmekretsnavn'])
    all_same = len(kretser) == 1 and kretser[0] == 'Hele kommunen'
    return area, all_same


def get_geojson_data(raw_data, kommuner):
    """Read in result files are produce corresponding geojson data."""
    results = read_csv_results(raw_data)

    all_geojson_data = []
    coordinates = []
    tooltips = []
    for kommune in kommuner:
        # Get results for each voting area:
        kommune_navn = results[
            results['Kommunenummer'] == kommune
        ]['Kommunenavn'].tolist()[0]
        print('Reading data for "{}"'.format(kommune_navn))
        area, all_same = extract_data(results, kommune)
        # Read the geojson file for this kommune:
        geojson_data = load_json_file(
            VALGKRETS_DIR.joinpath(VALGKRETS.format(kommune))
        )
        # Add results to the features:
        for feature in geojson_data['features']:
            if not all_same:
                krets = str(
                    feature['properties']['valgkretsnummer']
                ).rjust(4, '0')
            else:
                krets = '0000'
            feature['properties']['partinavn'] = area[krets]['partinavn']
            feature['properties']['oppslutning'] = '({:4.2f} %)'.format(
                area[krets]['oppslutning']
            )
            _add_coordinates(feature, coordinates)
        all_geojson_data.append((kommune_navn, geojson_data))
        tooltips.append(
            create_tool_tip(
                ('valgkretsnavn', 'partinavn', 'oppslutning'),
                ('Valgkrets:', 'Største parti:', 'Oppslutning (%):'),
                labels=False,
            )
        )
    map_settings = {
        'center': np.average(coordinates, axis=0)[::-1],
        'zoom': 10,
        'tooltip': tooltips,
    }
    return all_geojson_data, map_settings


def main(raw_data, kommuner):
    """Read input files and create the map."""
    geojson_data, map_settings = get_geojson_data(raw_data, kommuner)
    if len(kommuner) == 1:
        out = 'valgkretser-{}-{}.html'.format(
            kommuner[0], geojson_data[0][0]
        )
    else:
        out = 'map-valgkretser.html'
    produce_map(geojson_data, map_settings, output=out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
