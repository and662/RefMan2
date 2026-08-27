#!/bin/bash 

docker run --rm \
  --user="$(id -u):$(id -g)" \
  -v ".:/tmp/References" \
  -w "/tmp/References" \
  -it refman python3 .refman2/refman2.py "$@"

