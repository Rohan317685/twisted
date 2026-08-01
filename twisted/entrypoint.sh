#!/bin/sh
set -e

uv run manage.py migrate --noinput
python manage.py collectstatic --noinput


exec "$@"
