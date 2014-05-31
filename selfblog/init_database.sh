#!/bin/bash
nohup python manage.py syncdb --noinput > /dev/null 2>&1 &
sleep 5
nohup python manage.py loaddata dump-auth.json > /dev/null 2>&1 &
nohup python manage.py loaddata dump-blog.json > /dev/null 2>&1 &
