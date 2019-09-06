#!/bin/sh
exec gunicorn -b :5000 --timeout=1200 main:app --reload