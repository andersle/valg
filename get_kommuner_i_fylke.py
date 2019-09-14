# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Print the municipalities in a given county."""
import sys
from map_basics import read_csv_results


def main(raw_data, fylke_id):
    """Get the municipalities in a county."""
    results = read_csv_results(raw_data)
    data = results[results['Fylkenummer'] == fylke_id].groupby(
        ['Kommunenummer']
    )
    kommuner = [str(name) for name, _ in data]
    print(' '.join(kommuner))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
