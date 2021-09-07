#!/bin/bash
app="frontend.junco"
docker build -t ${app} .
docker run -it -d -p 8080:8080 \
  --name=${app} \
  -v $PWD:/app ${app}