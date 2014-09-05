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

```
curl -X POST -H "Content-Type: application/json" -d '{"conveyancer_lrid":"9c0250cd-dba7-4f7e-b7f5-5d526815bd28", "title_number":"DN100","clients":["b5fafd71-0c60-4a54-b7d0-bedcc8de358c", "fc3b9a32-5887-46e7-9885-c9dd30681f30"]}' localhost:8013/relationship
```

The response will be a randomly generated 4 digit code i.e. FKNY.
This code should be unique, but currently there is no check within the application to make sure it is. This is TODO.

Posting to /confirm will confirm that a client has accepted a relationship. An example post would be:

```
curl -X POST -H "Content-Type: application/json" -d '{"client_lrid":"b5fafd71-0c60-4a54-b7d0-bedcc8de358c", "code":"FKNY"}' localhost:8013/confirm
```
