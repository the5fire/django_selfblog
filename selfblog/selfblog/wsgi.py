import os

PROFILE = os.environ.get('DJANGOSELFBLOG_PROFILE', 'develop')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "selfblog.settings.%s" % PROFILE)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
