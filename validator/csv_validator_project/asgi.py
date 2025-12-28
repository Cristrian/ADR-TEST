"""
Configuración ASGI para el proyecto csv_validator_project.

Expone el objeto llamable ASGI como una variable a nivel de módulo llamada ``application``.

Para más información sobre este archivo, ver
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_validator_project.settings')

application = get_asgi_application()

