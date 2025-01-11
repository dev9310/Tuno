"""
WSGI config for musicplayer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicplayer.settings')
 
try :
    # from dj_static import Cling
    application = get_wsgi_application()
except Exception as e:
    print(e)
    


app = application