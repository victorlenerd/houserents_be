#!/bin/sh
$(aws ecr get-login --region us-east-2 --no-include-email)
docker pull 699011322781.dkr.ecr.us-east-2.amazonaws.com/houserents-api-develop:latest
docker run -d -p 5000:5000  \
    --env-file /home/ubuntu/.houserents-api-env \
    --name houserents-api \
    --rm 699011322781.dkr.ecr.us-east-2.amazonaws.com/houserents-api-develop:latest