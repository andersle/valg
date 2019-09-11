# valg

Mapping out the 2019 Norwegian local elections.

## Examples:

Note: The raw data is **not** included in this repository.

### Mapping results for voting areas

```bash
python map_valgkretser_i_kommune.py resultater_valgkretser/kommune-301-oslo.json
```
will generate the following map:

![oslo](/examples/oslo.png)

with html code as can be found [here](/examples/valgkretser-kommune-301-oslo.html).


```bash
python map_valgkretser_i_kommune.py resultater_valgkretser/kommune-5001-trondheim.json
```
will generate the following map:
![trondheim](/examples/trondheim.png)
with html code as can be found [here](examples/valgkretser-kommune-5001-trondheim.html).

### Mapping results for parties

```bash
python map_partier_i_valgkretser.py største_parti_valgkretser/*.json
```
will generate the following map:
![valgkretser](/examples/map-partier-valgkretser.png)

```bash
python map_partier_kommuner.py største_parti_kommuner/*.json
```
will generate the following map:
![kommuner](/examples/map-partier-kommuner.png)

## Sources

- For mapping: [Kartverket](https://kartkatalog.geonorge.no/metadata/kartverket/valgkretser/885225ca-a29f-4b22-95be-f886db66e4bb)

- For election results: [Valg](https://valgresultat.no/eksport-av-valgresultater?type=ko&year=2019)
