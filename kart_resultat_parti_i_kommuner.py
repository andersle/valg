# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing for which municipalities a given party is largest."""
import pathlib
import sys
from slugify import slugify
from map_basics import (
    produce_map,
    load_json_file,
    create_tool_tip,
    read_csv_results,
)


# Define paths to the raw geojson files:
KOMMUNE_DIR = pathlib.Path('kommuner')
KOMMUNE_KRETS = 'kommune-{}.geojson'


def extract_data(results, party):
    """Extract the data we want from the results."""
    area = {}
    alle_kommuner = [
        i for i in results.groupby(['Kommunenummer']).groups.keys()
    ]
    for kommune in alle_kommuner:
        kommune_data = results[results['Kommunenummer'] == kommune]
        idx = kommune_data['Oppslutning prosentvis'].idxmax()
        row = results.iloc[idx, :]
        if row['Partinavn'] == party:
            area[kommune] = {
                'partinavn': row['Partinavn'],
                'oppslutning': row['Oppslutning prosentvis'],
                'kommunenavn': row['Kommunenavn']
            }
    return area


def get_geojson_data(raw_data, parties):
    """Read in result files and produce corresponding geojson data."""
    results = read_csv_results(raw_data)
    all_geojson_data = []
    tooltip = []

    for party in parties:
        print('Adding for party "{}"'.format(party))
        new_data = {'features': []}
        area = extract_data(results, party)
        for kommune, kommune_data in area.items():
            print('Reading data for "{}"'.format(kommune_data['kommunenavn']))
            geojson_data = load_json_file(
                KOMMUNE_DIR.joinpath(KOMMUNE_KRETS.format(kommune))
            )
            for key in ('crs', 'type'):
                if key not in new_data:
                    new_data[key] = geojson_data[key]
            for feature in geojson_data['features']:
                feature['properties']['partinavn'] = kommune_data['partinavn']
                feature['properties']['kommunenavn'] = (
                    kommune_data['kommunenavn']
                )
                feature['properties']['oppslutning'] = '{:4.2f} %'.format(
                    kommune_data['oppslutning']
                )
                new_data['features'].append(feature)
        if new_data['features']:
            all_geojson_data.append((party, new_data))
            tooltip.append(
                create_tool_tip(
                    ('kommunenavn', 'partinavn', 'oppslutning'),
                    ('Kommune:', 'Største parti:', 'Oppslutning:'),
                    labels=False,
                )
            )
    map_settings = {
        'center': [63.0, 10.0],
        'zoom': 10,
        'tooltip': tooltip,
    }
    return all_geojson_data, map_settings


def main(raw_data, parties):
    """Read input files and create the map."""
    geojson_layers, map_settings = get_geojson_data(raw_data, parties)
    if len(parties) == 1:
        out = 'kommuner-{}.html'.format(slugify(parties[0]))
    else:
        out = 'map-partier-kommuner.html'
    produce_map(geojson_layers, map_settings, output=out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
