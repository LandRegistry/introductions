Land Registry Introductions Service
=========

[![Build Status](https://travis-ci.org/LandRegistry/introductions.svg)](https://travis-ci.org/LandRegistry/ownership)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/introductions.svg)](https://coveralls.io/r/LandRegistry/ownership)


This is the service that is responsible for storing the relationship between clients and conveyancers.

This application requires the following things:

```
python version 2.7
a postgres database called introductions.
```

To get started run the following command:

```
pip install -r requirements.txt
```

This application requires the following environment variables.

```
SETTINGS
DATABASE_URL
```

For local dev these are the settings.

```
export SETTINGS='config.DevelopmentConfig'
export DATABASE_URL='postgresql://localhost/introductions'
```

Start this application by running the following (note this will also upgrade the database tables):

```
./run.sh
```

This application currently has two end points: /relationship and /confirm

Posting to /relationship will set up a relationship between a conveyancer and a list
of clients. An example post would be:

Single client:
```
curl -X POST -H "Content-Type: application/json" -d '{"conveyancer_lrid":"214b78b1-20a0-4cdb-a0f3-111b5ba21d48", "title_number":"TEST1410429781566", "conveyancer_name": "Da Big Boss Company", "conveyancer_address": "123 High Street, Stoke, ST4 4AX", "clients":[{"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874", "name": "Walter White", "address": "1 The house, The town, PL1 1AA", "DOB": "01-01-1960", "tel_no": "01752 123456", "email": "citizen@example.org"}], "task":"sell"}' localhost:8013/relationship
```

Multiple clients:
```
curl -X POST -H "Content-Type: application/json" -d '{"conveyancer_lrid":"214b78b1-20a0-4cdb-a0f3-111b5ba21d48", "title_number":"TEST1410429781566", "conveyancer_name": "Da Big Boss Company", "conveyancer_address": "123 High Street, Stoke, ST4 4AX", "clients":[{"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874", "name": "Walter White", "address": "1 The house, The town, PL1 1AA", "DOB": "01-01-1960", "tel_no": "01752 123456", "email": "citizen@example.org"}, {"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874", "name": "Skyler White", "address": "1 The house, The town, PL1 1AA", "DOB": "04-06-1970", "tel_no": "01752 9999999", "email": "citizen2@example.org"}], "task":"sell"}' localhost:8013/relationship
```

The response will be a randomly generated 4 digit code i.e. FKNY.
This code should be unique, but currently there is no check within the application to make sure it is. This is TODO.

Posting to /confirm will confirm that a client has accepted a relationship. An example post would be:

```
curl -X POST -H "Content-Type: application/json" -d '{"client_lrid":"b5fafd71-0c60-4a54-b7d0-bedcc8de358c", "code":"FKNY"}' localhost:8013/confirm
```


To retrieve relationship details use your generated received from the /relationship call and post to the following end point.

```
curl -X POST -H "Content-Type: application/json" -d '{"token":"ZEHG"}' localhost:8013/details
```

The reponse willbe come JSON in the following format

```
{
    "property_town": "Plymouth",
    "conveyancer_address": "123 High Street, Stoke, ST4 4AX",
    "conveyancer_name": "Da Big Boss Company",
    "property_road": "The Road",
    "property_no": "56",
    "title_number": "TEST1410429781566",
    "task": "sell",
    "geometry": {
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        404439.5558898761,
                        369899.8484076261
                    ],
                    [
                        404440.0558898761,
                        369899.8484076261
                    ],
                    [
                        404440.0558898761,
                        369900.3484076261
                    ],
                    [
                        404439.5558898761,
                        369900.3484076261
                    ],
                    [
                        404439.5558898761,
                        369899.8484076261
                    ]
                ]
            ]
        },
        "crs": {
            "type": "name",
            "properties": {
                "name": "urn:ogc:def:crs:EPSG:27700"
            }
        },
        "type": "Feature",
        "properties": {
            "Description": "Polygon"
        }
    },
    "property_postcode": "PL1 1AA",
    "clients": [
        {
            "lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874",
            "name": "Walter White",
            "DOB": "01-01-1960",
            "address": "1 The house, The town, PL1 1AA",
            "tel_no": "01752 123456",
            "email": "citizen@example.org"
        },
        {
            "lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874",
            "name": "Skyler White",
            "DOB": "04-06-1970",
            "address": "1 The house, The town, PL1 1AA",
            "tel_no": "01752 9999999",
            "email": "citizen2@example.org"
        }
    ],
    "conveyancer_lrid": "214b78b1-20a0-4cdb-a0f3-111b5ba21d48"
}
```
