#!/bin/sh
docker run -d -p 5000:5000  \
    --env-file ./.houserents-api-env
    --rm 699011322781.dkr.ecr.us-east-2.amazonaws.com/houserents-fe-develop:latest