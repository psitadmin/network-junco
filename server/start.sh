#!/bin/bash
app="backend.junco"
docker build -t ${app} .
docker run -it -d -p 5000:5000 \
  --name=${app} \
  -v $PWD:/app ${app}