#!/bin/bash

. env/bin/activate
exec gunicorn_django -b 127.0.0.1:8083 live_settings.py
