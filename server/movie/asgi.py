import os
import django
from channels.routing import get_default_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie.settings')
django.setup()
application = get_asgi_application()
