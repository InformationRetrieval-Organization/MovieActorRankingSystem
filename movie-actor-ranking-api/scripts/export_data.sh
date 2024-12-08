#!/bin/bash

# Variables
CONTAINER_NAME=movieactorrankingpostgres
DATABASE_NAME=movieactorrankingdb
USERNAME=postgres
OUTPUT_FILE=database_dump.sql

# Export the data
docker exec -t $CONTAINER_NAME pg_dump -U $USERNAME -d $DATABASE_NAME -F c -b -v -f  /tmp/$OUTPUT_FILE

# Copy the dump file to the local machine
docker cp $CONTAINER_NAME:/tmp/$OUTPUT_FILE .

# Add the dump file to the repository
WORKSPACE=$(pwd)
OUTPUT_FILE=$WORKSPACE/$OUTPUT_FILE
