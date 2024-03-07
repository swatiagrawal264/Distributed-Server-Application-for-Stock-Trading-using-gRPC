#!/bin/bash

# build the first image
docker build -t frontendimage -f Dockerfile_frontend .

# build the second image
docker build -t catalogimage -f Dockerfile_Catalog .

# build the third image
docker build -t orderimage -f Dockerfile_Order .
