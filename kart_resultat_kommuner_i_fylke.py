# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing the largest party in different voting areas."""
import pathlib
import sys
import numpy as np
from slugify import slugify
from map_basics import (
    produce_map,
    load_json_file,
    create_tool_tip,
    read_csv_results,
)


# Define paths to the raw geojson files:
KOMMUNE_DIR = pathlib.Path('kommuner')
KOMMUNE = 'kommune-{}.geojson'


def _add_coordinates(feature, coordinates):
    """Add coordinates from a feature."""
    coords = []
    for polygon in feature['geometry']['coordinates']:
        for row in polygon:
            coords.append(row)
    coordinates.append(np.average(coords, axis=0))


def extract_data(results, fylke):
    """Extract the data we want from the results."""
    data = results[results['Fylkenummer'] == fylke]
    fylke_data = data.groupby(['Kommunenummer'])
    fylke_navn = data['Fylkenavn'].tolist()[0]
    area = {}
    for name, group in fylke_data:
        idx = group['Oppslutning prosentvis'].idxmax()
        maxi = results.iloc[idx, :]
        area[name] = {
            'partinavn': maxi['Partinavn'],
            'oppslutning': maxi['Oppslutning prosentvis'],
            'kommune': maxi['Kommunenavn'],
            'fylke': maxi['Fylkenavn'],
        }
    return area, fylke_navn


def get_geojson_data(raw_data, fylker):
    """Read in result files are produce corresponding geojson data."""
    results = read_csv_results(raw_data)

    all_geojson_data = []
    coordinates = []
    tooltips = []
    fylker_navn = []
    for fylke in fylker:
        area, fylke_navn = extract_data(results, fylke)
        print('Reading for "{}"'.format(fylke_navn))
        fylker_navn.append(fylke_navn)
        for kommune, kommune_data in area.items():
            # Read the geojson file for this kommune:
            geojson_data = load_json_file(
                KOMMUNE_DIR.joinpath(KOMMUNE.format(kommune))
            )
            # Add results to the features:
            for feature in geojson_data['features']:
                feature['properties']['partinavn'] = kommune_data['partinavn']
                feature['properties']['oppslutning'] = '({:4.2f} %)'.format(
                    kommune_data['oppslutning']
                )
                feature['properties']['kommunenavn'] = kommune_data['kommune']
                _add_coordinates(feature, coordinates)
            all_geojson_data.append((kommune_data['kommune'], geojson_data))
            tooltips.append(
                create_tool_tip(
                    ('kommunenavn', 'partinavn', 'oppslutning'),
                    ('Kommune:', 'Største parti:', 'Oppslutning (%):'),
                    labels=False,
                )
            )
    map_settings = {
        'center': np.average(coordinates, axis=0)[::-1],
        'zoom': 10,
        'tooltip': tooltips,
    }
    return all_geojson_data, map_settings, fylker_navn


def main(raw_data, fylker):
    """Read input files and create the map."""
    geojson_data, map_settings, fylker_navn = get_geojson_data(
        raw_data, fylker
    )
    idx = '-'.join(['{}'.format(i) for i in fylker])
    navn = '-'.join([slugify(i) for i in fylker_navn])
    out = 'resultat-{}-{}.html'.format(
        idx, navn
    )
    produce_map(geojson_data, map_settings, output=out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
