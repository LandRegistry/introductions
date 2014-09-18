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
curl -X POST -H "Content-Type: application/json" -d '{"conveyancer_lrid":"214b78b1-20a0-4cdb-a0f3-111b5ba21d48", "title_number":"TEST1410429781566", "conveyancer_name": "Da Big Boss Company", "conveyancer_address": "123 High Street, Stoke, ST4 4AX", "clients":[{"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874"}], "task":"sell"}' localhost:8013/relationship
```

Multiple clients:
```
curl -X POST -H "Content-Type: application/json" -d '{"conveyancer_lrid":"214b78b1-20a0-4cdb-a0f3-111b5ba21d48", "title_number":"TEST1410429781566", "conveyancer_name": "Da Big Boss Company", "conveyancer_address": "123 High Street, Stoke, ST4 4AX", "clients":[{"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874"}, {"lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874"}], "task":"sell"}' localhost:8013/relationship
```

The response will be a randomly generated 4 digit code i.e. FKNY.
This code should be unique, but currently there is no check within the application to make sure it is. This is TODO.

Posting to /confirm will confirm that a client has accepted a relationship. An example post would be:

```
curl -X POST -H "Content-Type: application/json" -d '{"client_lrid":"b5fafd71-0c60-4a54-b7d0-bedcc8de358c", "token":"FKNY"}' localhost:8013/confirm
```


To retrieve relationship details use your generated received from the /relationship call and post to the following end point.

```
curl http://localhost:8013/details/FKNY
```

The reponse willbe come JSON in the following format.

```
{
    "task": "sell",
    "conveyancer_address": "123 High Street, Stoke, ST4 4AX",
    "conveyancer_name": "Da Big Boss Company",
    "client_lrid": "f55a02a0-057b-4a3f-9e34-ede5791a5874",
    "title_number": "TEST1410429781566",
    "conveyancer_lrid": "214b78b1-20a0-4cdb-a0f3-111b5ba21d48"
}
```
