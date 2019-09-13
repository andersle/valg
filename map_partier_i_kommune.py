# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing voting areas with the results for a party."""
import pathlib
import sys
import pandas as pd
import numpy as np
from map_basics import create_folium_choropleth, load_json_file


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


def get_geojson_data(result_file, kommune_id):
    """Read in result files are produce corresponding geojson data."""
    print('Reading file "{}"'.format(result_file))

    data = load_json_file(result_file)
    print('Read data for party "{}"'.format(data['navn']))

    kommune_data = data['kommuner'][kommune_id]

    print(
        'Picked results for kommune {}: "{}"'.format(
            kommune_id,
            kommune_data['kommune_navn']
        )
    )

    geojson_data = _load_geojson_file(kommune_id.rjust(4, '0'))

    raw_data = {}
    for key in ('krets', 'oppslutning_prosentvis', 'krets_navn'):
        raw_data[key] = kommune_data[key]

    missing = 0.0
    if raw_data['krets_navn'][0] == 'Hele kommunen':
        missing = raw_data['oppslutning_prosentvis'][0]

    # Check that we have data for all features:
    for feature in geojson_data['features']:
        krets = feature['properties']['valgkretsnummer']
        if krets not in raw_data['krets']:
            print('Missing area "{}"'.format(krets))
            raw_data['krets'].append(krets)
            raw_data['oppslutning_prosentvis'].append(missing)
            raw_data['krets_navn'] = 'Missing data'

    results = pd.DataFrame.from_dict(raw_data)

    map_settings = {
        'title': kommune_data['kommune_navn'],
        'party': data['navn'],
        'center': get_center(geojson_data['features'])[::-1],
        'zoom': 10,
    }
    return geojson_data, results, map_settings


def main(result_file, kommune_id):
    """Read input file and create the map."""
    geojson_data, results, map_settings = get_geojson_data(
        result_file, kommune_id
    )
    the_map = create_folium_choropleth(geojson_data, results, map_settings)

    filename = pathlib.Path(result_file).stem
    out = '{}-kommune-{}-{}.html'.format(
        filename, kommune_id, map_settings['title']
    )
    print('Writing map to "{}"'.format(out))
    the_map.save(out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
