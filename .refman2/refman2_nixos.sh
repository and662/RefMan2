#!/run/current-system/sw/bin/bash

docker run --rm \
  --user="$(id -u):$(id -g)" \
  -v "..:/tmp/References" \
  -w "/tmp/References/.refman2" \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -it refman python3 "$@"


