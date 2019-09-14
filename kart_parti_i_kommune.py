# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing voting areas with the results for a party."""
import pathlib
import sys
import pandas as pd
from slugify import slugify
import numpy as np
from map_basics import (
    create_folium_choropleth,
    load_json_file,
    create_tool_tip,
    read_csv_results,
)


VALGKRETS_DIR = pathlib.Path('valgkretser')
VALGKRETS = 'krets-{}.geojson'


def _load_geojson_file(kommune_id):
    """Load data from a geojson file."""
    geojson_file = VALGKRETS_DIR.joinpath(
        VALGKRETS.format(kommune_id)
    )
    return load_json_file(geojson_file)


def get_center(features):
    """Calculate the geometric center for some features."""
    averages = []
    for feature in features:
        for polygon in feature['geometry']['coordinates']:
            coord = np.array(polygon)
            averages.append(np.average(coord, axis=0))
    averages = np.array(averages)
    return np.average(averages, axis=0)


def extract_data(results, kommune_id, party):
    """Extract the required data."""
    kommune_data = results[results['Kommunenummer'] == kommune_id]
    parti_data = kommune_data[kommune_data['Partinavn'] == party]
    raw_data = {}
    kretser = []
    for _, row in parti_data.iterrows():
        raw_data[row['Stemmekretsnummer']] = {
            'krets': row['Stemmekretsnavn'],
            'partinavn': row['Partinavn'],
            'oppslutning': row['Oppslutning prosentvis'],
            'kommunenavn': row['Kommunenavn'],
        }
        kretser.append(row['Stemmekretsnavn'])
    all_same = len(kretser) == 1 and kretser[0] == 'Hele kommunen'
    return raw_data, all_same


def get_geojson_data(result_file, party, kommune_id):
    """Read in result files are produce corresponding geojson data."""
    results = read_csv_results(result_file)
    kommune_data = results[results['Kommunenummer'] == kommune_id]
    kommune_navn = kommune_data['Kommunenavn'].tolist()[0]
    print('Reading data for "{}" in "{}"'.format(party, kommune_navn))
    raw_data, all_same = extract_data(results, kommune_id, party)
    geojson_data = _load_geojson_file(kommune_id)
    # Check that we have data for all features:
    for feature in geojson_data['features']:
        if not all_same:
            krets = str(
                feature['properties']['valgkretsnummer']
            ).rjust(4, '0')
        else:
            krets = '0000'
        feature['properties']['oppslutning'] = '({:4.2f} %)'.format(
            raw_data[krets]['oppslutning']
        )
        feature['properties']['partinavn'] = raw_data[krets]['partinavn']
        feature['properties']['krets'] = krets
    map_settings = {
        'title': kommune_navn,
        'party': party,
        'center': get_center(geojson_data['features'])[::-1],
        'zoom': 10,
        'value_key': 'oppslutning',
        'tooltip': create_tool_tip(
            ('valgkretsnavn', 'partinavn', 'oppslutning'),
            ('Krets:', 'Parti', 'Oppslutning (%)'),
            labels=False,
        )
    }
    return geojson_data, raw_data, map_settings


def main(result_file, party, kommune_id):
    """Read input file and create the map."""
    geojson_data, results, map_settings = get_geojson_data(
        result_file, party, kommune_id
    )
    the_map = create_folium_choropleth(geojson_data, results, map_settings)

    out = 'stemmekrester-{}-kommune-{}-{}.html'.format(
        slugify(party), kommune_id, slugify(map_settings['title'])
    )
    print('Writing map to "{}"'.format(out))
    the_map.save(out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])
