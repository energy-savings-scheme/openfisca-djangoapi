#!/usr/bin/env bash

# Run the `docker-compose run` commands in the docker shell environment
# This mirrors the local dev docker workflow.

sudo docker-compose run app setup_db
sudo docker-compose run app fetch_data
