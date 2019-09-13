# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map showing for which municipalities a given party is largest."""
import pathlib
import sys
import pandas as pd
from map_basics import produce_map, load_json_file, create_tool_tip


# Define paths to the raw geojson files:
KOMMUNE_DIR = pathlib.Path('kommuner')
KOMMUNE_KRETS = 'kommune-{}.geojson'


def get_geojson_data(result_files):
    """Read in result files and produce corresponding geojson data."""
    all_geojson_data = []
    tooltip = []
    for result_file in result_files:
        print('Reading file "{}"'.format(result_file))
        new_data = {'features': []}
        results = pd.read_json(result_file)
        # The input data is assumed to be structured so that it only
        # contains data for one party:
        parti = results['Partinavn'].tolist()[0]
        for _, row in results.iterrows():
            kommune = str(int(row['Kommunenummer']))
            oppslutning = row['Oppslutning prosentvis']
            kommune_id = '{}'.format(kommune).rjust(4, '0')
            geojson_file = KOMMUNE_DIR.joinpath(
                KOMMUNE_KRETS.format(kommune_id)
            )
            geojson_data = load_json_file(geojson_file)
            for key in ('crs', 'type'):
                if key not in new_data:
                    new_data[key] = geojson_data[key]
            for feature in geojson_data['features']:
                feature['properties']['partinavn'] = parti
                feature['properties']['kommunenavn'] = (
                    feature['properties']['navn'][0]['navn']
                )
                feature['properties']['oppslutning'] = '{:4.2f} %'.format(
                    oppslutning
                )
                new_data['features'].append(feature)
        if new_data['features']:
            all_geojson_data.append((parti, new_data))
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


def main(result_files):
    """Read input files and create the map."""
    geojson_layers, map_settings = get_geojson_data(result_files)
    if len(result_files) == 1:
        filename = pathlib.Path(result_files[0]).stem
        out = '{}.html'.format(filename)
    else:
        out = 'map-partier-kommuner.html'
    produce_map(geojson_layers, map_settings, output=out)


if __name__ == '__main__':
    main(sys.argv[1:])
