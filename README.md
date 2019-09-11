# valg

Mapping out the [2019 Norwegian local elections](https://en.wikipedia.org/wiki/2019_Norwegian_local_elections).

## Examples:

Note: The raw data is **not** included in this repository.

### Mapping results for voting areas

To map the results in the voting areas in municipalities, the script
[map_valgkretser_i_kommune.py](map_valgkretser_i_kommune.py) is used:

```bash
python map_valgkretser_i_kommune.py resultater_valgkretser/kommune-301-oslo.json
```
which will generate the following map:

![oslo](/examples/oslo.png)

Another example:


```bash
python map_valgkretser_i_kommune.py resultater_valgkretser/kommune-5001-trondheim.json
```
witch will generate the following map:
![trondheim](/examples/trondheim.png)

### Mapping results for parties

To map results for individual parties, the script
[map_partier_i_valgkretser.py](map_partier_i_valgkretser.py) can be
used to display the voting areas where a given party got the most votes:

```bash
python map_partier_i_valgkretser.py største_parti_valgkretser/*.json
```
will generate the following map:
![valgkretser](/examples/map-partier-valgkretser.png)

To map out similar results, but for municipalities, the script
[map_partier_kommuner.py](map_partier_kommuner.py) is used:

```bash
python map_partier_kommuner.py største_parti_kommuner/*.json
```
witch will generate the following map:
![kommuner](/examples/map-partier-kommuner.png)

## Sources

- For mapping: [Kartverket](https://kartkatalog.geonorge.no/metadata/kartverket/valgkretser/885225ca-a29f-4b22-95be-f886db66e4bb)

- For election results: [Valg](https://valgresultat.no/eksport-av-valgresultater?type=ko&year=2019)
