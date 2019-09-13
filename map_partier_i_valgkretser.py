# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing voting areas where a given party is largest."""
import pathlib
import sys
import pandas as pd
from map_basics import produce_map, COLORS_PARTY, load_json_file


VALGKRETS_DIR = pathlib.Path('valgkretser')
VALGKRETS = 'krets-{}.geojson'


def _load_geojson_file(kommune_id):
    """Load data from a geojson file."""
    geojson_file = VALGKRETS_DIR.joinpath(
        VALGKRETS.format(kommune_id)
    )
    return load_json_file(geojson_file)


def _add_dict_keys(keys, from_dict, others):
    """Add values from a dictionary to others."""
    for key in keys:
        for to_dict in others:
            if key not in to_dict:
                to_dict[key] = from_dict[key]


def get_geojson_data(result_files):
    """Read in result files are produce corresponding geojson data."""
    all_geojson_data = []
    andre = {'features': []}
    for result_file in result_files:
        print('Reading file "{}"'.format(result_file))
        results = pd.read_json(result_file)
        kommuner = results['Kommunenummer'].tolist()
        kretser = results['Stemmekretsnummer'].tolist()
        kretser_navn = results['Stemmekretsnavn'].tolist()
        # Each file is assumed to only contain results for one party:
        parti = results['Partinavn'].tolist()[0]

        new_data = {'features': []}
        for kommune, krets, krets_navn in zip(kommuner, kretser, kretser_navn):
            kommune_id = '{}'.format(kommune).rjust(4, '0')
            geojson_data = _load_geojson_file(kommune_id)
            _add_dict_keys(('crs', 'type'), geojson_data, (new_data, andre))

            for feature in geojson_data['features']:
                nummer = feature['properties']['valgkretsnummer']
                if krets_navn == 'Hele kommunen' or nummer == krets:
                    feature['properties']['partinavn'] = parti
                    if parti in COLORS_PARTY:
                        new_data['features'].append(feature)
                    else:
                        andre['features'].append(feature)
        if new_data['features'] and parti in COLORS_PARTY:
            all_geojson_data.append((parti, new_data))
    if andre['features']:
        all_geojson_data.append(('Andre', andre))
    return all_geojson_data


def main(result_files):
    """Read input files and create the map."""
    geojson_data = get_geojson_data(result_files)
    if len(result_files) == 1:
        filename = pathlib.Path(result_files[0]).stem
        out = 'valgkretser-{}.html'.format(filename)
    else:
        out = 'map-partier-valgkretser.html'
    produce_map(geojson_data, [63.446827, 10.421906], 10, output=out)


if __name__ == '__main__':
    main(sys.argv[1:])
