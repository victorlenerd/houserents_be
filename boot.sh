#!/bin/sh
exec gunicorn -b :$PORT --timeout=1200 --log-level=debug --access-logfile - --error-logfile - main:app