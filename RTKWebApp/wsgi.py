"""
WSGI config for RTKWebApp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append('/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects/RTKWebApp/')
os.environ.setdefault("PYTHON_EGG_CACHE", "/home/republicuser/djangostack-2.0.3-0/apps/django/django_projects/RTKWebApp/egg_cache")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RTKWebApp.settings")

application = get_wsgi_application()

