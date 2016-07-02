#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    PROFILE = os.environ.get('DJANGOSELFBLOG_PROFILE', 'develop')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfblog.settings.%s" % PROFILE)
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
