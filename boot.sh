#!/bin/sh
exec gunicorn -b :5000 --timeout=1200 --log-level=debug --access-logfile - --error-logfile - main:app