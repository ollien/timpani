#!/bin/bash

docker pull ollien/postgres
docker run -d --name="postgres" -p 127.0.0.01:54320:5432 -p 127.0.0.1:54330:5433 postgres
docker start postgres

mkdir configs
echo '{"connection_string": "postgresql://root@127.0.0.1:54320/blog"}' > configs/database.json
echo '{"display_full_name": true}' > configs/templates.json
cd $(dirname "$BASH_SOURCE")
python3 ./travis-setup.py
