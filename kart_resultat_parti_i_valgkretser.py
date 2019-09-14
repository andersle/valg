# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing voting areas where a given party is largest."""
import pathlib
import sys
from slugify import slugify
from map_basics import (
    produce_map,
    COLORS_PARTY,
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


def _add_dict_keys(keys, from_dict, others):
    """Add values from a dictionary to others."""
    for key in keys:
        for to_dict in others:
            if key not in to_dict:
                to_dict[key] = from_dict[key]


def extract_data(results, party):
    """Extract the data we want from the results."""
    area = {}
    alle_kommuner = [
        i for i in results.groupby(['Kommunenummer']).groups.keys()
    ]
    for kommune in alle_kommuner:
        kommune_data = results[results['Kommunenummer'] == kommune].groupby(
            ['Stemmekretsnummer']
        )
        for name, group in kommune_data:
            idx = group['Oppslutning prosentvis'].idxmax()
            maxi = results.iloc[idx, :]
            if maxi['Partinavn'] == party:
                if kommune not in area:
                    area[kommune] = {}
                area[kommune][name] = {
                    'partinavn': maxi['Partinavn'],
                    'oppslutning': maxi['Oppslutning prosentvis'],
                    'krets': maxi['Stemmekretsnavn'],
                    'kommune_navn': maxi['Kommunenavn']
                }
    return area


def _same_for_all(kretser):
    """Check if the result it for the whole municipality."""
    for _, krets_data in kretser.items():
        if krets_data['krets'] == 'Hele kommunen':
            return True, krets_data
    return False, None


def add_to_features(features, kretser, party):
    """Add data from the areas to the features."""
    same_all, krets_data = _same_for_all(kretser)
    for feature in features:
        krets = str(
            feature['properties']['valgkretsnummer']
        ).rjust(4, '0')
        if not same_all:
            if krets in kretser:
                krets_data = kretser[krets]
            else:
                krets_data = None
        if krets_data is not None:
            feature['properties']['use_this_feature'] = True
            feature['properties']['partinavn'] = party
            feature['properties']['oppslutning'] = (
                '({:4.2f} %)'.format(
                    krets_data['oppslutning']
                )
            )


def get_geojson_data(raw_data, parties):
    """Read in result files are produce corresponding geojson data."""
    results = read_csv_results(raw_data)
    all_geojson_data = []
    andre = {'features': []}
    tooltip = []

    for party in parties:
        print('Adding for party "{}"'.format(party))
        new_data = {'features': []}
        area = extract_data(results, party)
        for kommune, kretser in area.items():
            geojson_data = _load_geojson_file(kommune)
            _add_dict_keys(('crs', 'type'), geojson_data, (new_data, andre))
            add_to_features(geojson_data['features'], kretser, party)
            for feature in geojson_data['features']:
                if 'use_this_feature' in feature['properties']:
                    if party in COLORS_PARTY:
                        new_data['features'].append(feature)
                    else:
                        andre['features'].append(feature)
        if new_data['features'] and party in COLORS_PARTY:
            all_geojson_data.append((party, new_data))
            tooltip.append(
                create_tool_tip(
                    ('valgkretsnavn', 'partinavn', 'oppslutning'),
                    ('Valgkrets:', 'Største parti:', 'Oppslutning (%)'),
                    labels=False,
                )
            )
    if andre['features']:
        all_geojson_data.append(('Andre', andre))
        tooltip.append(
            create_tool_tip(
                ('valgkretsnavn', 'partinavn', 'oppslutning'),
                ('Valgkrets:', 'Største parti:', 'Oppslutning (%)'),
                labels=False,
            )
        )
    map_settings = {
        'center': [63.446827, 10.421906],
        'zoom': 10,
        'tooltip': tooltip,
    }
    return all_geojson_data, map_settings


def main(raw_data, parties):
    """Read input files and create the map."""
    geojson_data, map_settings = get_geojson_data(raw_data, parties)
    if len(parties) == 1:
        out = 'valgkretser-{}.html'.format(slugify(parties[0]))
    else:
        out = 'map-partier-valgkretser.html'
    produce_map(geojson_data, map_settings, output=out)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
