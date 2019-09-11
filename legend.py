# Copyright (c) 2019, Anders Lervik.
# Distributed under the MIT License. See LICENSE for more info.
"""Add a Legend to a folium map.

This code is based on:

https://nbviewer.jupyter.org/gist/talbertc-usgs/18f8901fc98f109f2b71156cf3ac81cd
"""
from branca.element import CssLink, Figure, MacroElement
from jinja2 import Template


CSSURL = 'legend.css'


class Legend(MacroElement):
    """Add a legend to a Leaflet map."""

    _template = Template("""
        {% macro html(this,kwargs) %}
        <div id='maplegend' class='maplegend'
            style='position: absolute;
            z-index:9999;
            border:2px solid grey;
            background-color:rgba(255, 255, 255, 0.8);
            border-radius:6px;
            padding: 10px;
            font-size:14px;
            right: 20px;
            bottom: 20px;'>

            <div class='legend-title'>{{this.title}}</div>
            <div class='legend-scale'>
                <ul class='legend-labels'>
                {% for label in this.labels %}
                    <li><span style='background:{{label.color}};opacity:{{label.opacity}};'></span>{{label.text}}</li>
                {% endfor %}
                </ul>
            </div>
        </div>
        {% endmacro %}
        """)

    def __init__(self, title, labels):
        """Set up the legend.

        Parameters
        ----------
        title : string
            The title to use for the legend box.
        labels : list of dicts
            The dicts defining the labels. Each dict contains a
            'text', 'color' and 'opacity' which is used in the legend.

        """
        super().__init__()
        self._name = 'Legend'
        self.title = title
        self.labels = labels

    def render(self, **kwargs):
        """Render the legend."""
        super().render(**kwargs)

        figure = self.get_root()
        assert isinstance(figure, Figure), ('You cannot render this Element '
                                            'if it is not in a Figure.')
        figure.header.add_child(CssLink(CSSURL), name='legend_css')
