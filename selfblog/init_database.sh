#!/bin/bash
nohup python manage.py syncdb --noinput > /dev/null 2>&1 &
nohup python manage.py loaddata initial_data.json > /dev/null 2>&1 &
