#!/bin/bash 

docker run --rm \
  --user="$(id -u):$(id -g)" \
  -v "..:/tmp/References" \
  -w "/tmp/References/.refman2" \
  -it refman python3 "$@"


