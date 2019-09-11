# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Create a map using folium."""
import folium
from legend import Legend


COLORS = {
    'blue': '#1f77b4',
    'orange': '#ff7f0e',
    'green': '#2ca02c',
    'red': '#d62728',
    'purple': '#9467bd',
    'brown': '#8c564b',
    'pink': '#e377c2',
    'gray': '#7f7f7f',
    'yellow': '#bcbd22',
    'cyan': '#17becf',
}


COLORS_PARTY = {
    'Arbeiderpartiet': COLORS['red'],
    'Høyre': COLORS['blue'],
    'Miljøpartiet De Grønne': COLORS['green'],
    'Senterpartiet': COLORS['yellow'],
    'SV - Sosialistisk Venstreparti': COLORS['pink'],
    'Fremskrittspartiet': COLORS['brown'],
    'Venstre': COLORS['orange'],
    'Folkeaksjonen Nei til mer bompenger': COLORS['gray'],
    'Kristelig Folkeparti': COLORS['cyan'],
    'Rødt': COLORS['purple'],
    'Andre': '#262626',
}


TILES = [
    {
        'name': 'topo4graatone',
        'url': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4graatone&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    },
    {
        'name': 'topo4',
        'url': (
            'http://opencache.statkart.no/gatekeeper/gk/gk.open_gmaps?'
            'layers=topo4&zoom={z}&x={x}&y={y}'
        ),
        'attr': (
            '<a href="http://www.kartverket.no/">Kartverket</a>',
        ),
    },
]


OPACITY = 0.7


def default_style_function(item):
    """Style for geojson polygons."""
    party = item['properties']['partinavn']
    if party not in COLORS_PARTY:
        print('Missing color for {} --- using default'.format(party))
    style = {
        'fillColor': COLORS_PARTY.get(party, '#262626'),
        'fillOpacity': OPACITY,
        'color': '#262626',
        'weight': 0.5,
    }
    return style


def add_tiles_to_map(the_map):
    """Add default tiles to a folium map.

    Parameters
    ----------
    the_map : object like folium.folium.Map
        The map we are to add the tiles to.

    """
    for tile in TILES:
        folium.TileLayer(
            tile['url'], attr=tile['attr'], name=tile['name']
        ).add_to(the_map)
    folium.TileLayer('openstreetmap').add_to(the_map)


def add_legend_to_map(the_map):
    """Add a default legend to a folium map.

    Parameters
    ----------
    the_map : object like folium.folium.Map
        The map we are to add the tiles to.

    """
    labels = []
    for key, val in COLORS_PARTY.items():
        labels.append({'text': key, 'color': val, 'opacity': OPACITY})
    legend = Legend(title='Partier', labels=labels)
    the_map.add_child(legend)


def add_geojson_layers(the_map, geojson_layers,
                       style_function=default_style_function):
    """Add geojson layers to a map.

    Parameters
    ----------
    geojson_layers : list of tuples
        Each typle is of form (name, geojson-dict) where the
        name is used as a label and the geojson-dict contains
        the geojson layer to be shown.
    style_function : callable, optional
        A style function for defining the style to use when drawing
        the geojson layers.

    """
    for name, data in geojson_layers:
        folium.GeoJson(
            data,
            name=name,
            style_function=style_function
        ).add_to(the_map)


def create_folium_map(geojson_layers, map_settings):
    """Create a folium map.

    Parameters
    ----------
    geojson_layers : list of tuples
        Each typle is of form (name, geojson-dict) where the
        name is used as a label and the geojson-dict contains
        the geojson layer to be shown.
    map_settings : dict
        A dict containing settings for initializing the map.

    Returns
    -------
    the_map : object like folium.folium.Map
        The map created here.

    """
    the_map = folium.Map(
        location=map_settings.get('center', [63.447, 10.422]),
        tiles=None,
        zoom_start=map_settings.get('zoom', 9),
    )
    add_tiles_to_map(the_map)
    add_geojson_layers(the_map, geojson_layers)
    folium.LayerControl().add_to(the_map)
    add_legend_to_map(the_map)
    return the_map


def produce_map(geojson_layers, center, zoom, output='map.html'):
    """Produce the folium map and save it to a file.

    Parameters
    ----------
    geojson_layers : list of tuples
        Each typle is of form (name, geojson-dict) where the
        name is used as a label and the geojson-dict contains
        the geojson layer to be shown.
    center : tuple of floats
        The initial center of the folium map.
    zoom : int
        The initial zoom level of the folium map.
    output : string, optional
        The file name to write the map to.

    """
    map_settings = {'center': center, 'zoom': zoom}
    the_map = create_folium_map(geojson_layers, map_settings)
    print('Writing map to: {}'.format(output))
    the_map.save(output)
