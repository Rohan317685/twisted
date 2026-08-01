#!/bin/sh
set -e

uv run manage.py migrate --noinput

exec "$@"
