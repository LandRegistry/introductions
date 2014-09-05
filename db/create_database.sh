#!/bin/bash

createuser -s introductions
createdb -U introductions -O introductions introductions -T template0
