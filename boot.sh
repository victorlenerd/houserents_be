#!/bin/sh
exec gunicorn -b :$PORT --timeout=1200 main:app --reload