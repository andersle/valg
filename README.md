# valg

Mapping out the [2019 Norwegian local elections](https://en.wikipedia.org/wiki/2019_Norwegian_local_elections).

## Examples:

Note: The raw data is **not** included in this repository.
Please see the [sources](#sources) given below.


### Mapping results for a party in voting areas

To map results in the voting area in municipalities for a given party, the
script [kart_parti_i_kommune.py](kart_parti_i_kommune.py) is used:

```bash
python kart_parti_i_kommune.py 2019-09-14_partifordeling_4_ko_2019.csv "Folkeaksjonen Nei til mer bompenger" 0301
```
which will generate the following map:

![oslofnb](/examples/oslofnb.png)

Another example:

```bash
python kart_parti_i_kommune.py 2019-09-14_partifordeling_4_ko_2019.csv "Miljøpartiet De Grønne" 5001
```

which will generate the following map:
![trondheimmdg](/examples/trondheimmdg.png)


### Mapping the largest party in voting areas in municipalities

To map the largest parties in the voting areas in municipalities, the script
[kart_resultat_valgkretser_i_kommune.py](kart_resultat_valgkretser_i_kommune.py) is used:


```bash
python kart_resultat_valgkretser_i_kommune.py 2019-09-14_partifordeling_4_ko_2019.csv 0301
```
which will generate the following map:

![oslo](/examples/oslo.png)


Another example:

```bash
python kart_resultat_valgkretser_i_kommune.py 2019-09-14_partifordeling_4_ko_2019.csv 5001
```

witch will generate the following map:

![trondheim](/examples/trondheim.png)

And another example:

```bash
python kart_resultat_valgkretser_i_kommune.py 2019-09-14_partifordeling_4_ko_2019.csv 4601 4627 4630
```
which will generate the following map:

![bergen](/examples/bergen.png)

As shown above, the script accepts multiple values for the municipality. One can
for instance create a full map for the whole of Norway:

![valgkretser](/examples/map-partier-valgkretser.png)


### Mapping results for parties

To map results for individual parties, the script
[kart_resultat_parti_i_valgkretser.py](kart_resultat_parti_i_valgkretser.py) can be
used to display the voting areas where a given party got the most votes:

```bash
python kart_resultat_parti_i_valgkretser.py 2019-09-14_partifordeling_4_ko_2019.csv "Folkeaksjonen Nei til mer bompenger" "Fremskrittspartiet"
```
witch will generate the following map:

![bompenger](/examples/bom.png)

To map out similar results, but for municipalities, the script
[kart_resultat_parti_i_kommuner.py](kart_resultat_parti_i_kommuner.py) is used:

```bash
python kart_resultat_parti_i_kommuner.py 2019-09-14_partifordeling_2_ko_2019.csv Arbeiderpartiet Høyre Senterpartiet
```
witch will generate the following map:

![kommuner](/examples/map-partier-kommuner.png)


### Mapping results for county councils

To map results for county councils the script
[kart_resultat_kommuner_i_fylke.py](kart_resultat_kommuner_i_fylke.py) is used: 

```bash
python kart_resultat_kommuner_i_fylke.py 2019-09-14_partifordeling_2_ko_2019.csv 50
```

which will generate the following map:

![trondelag](/examples/trondelag.png)


## Sources

- For mapping: [Kartverket](https://kartkatalog.geonorge.no/metadata/kartverket/valgkretser/885225ca-a29f-4b22-95be-f886db66e4bb)

- For election results: [Valg](https://valgresultat.no/eksport-av-valgresultater?type=ko&year=2019)
