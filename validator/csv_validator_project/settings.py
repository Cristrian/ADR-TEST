"""
Configuración de Django para el proyecto csv_validator_project.
"""

from pathlib import Path

# Construir rutas dentro del proyecto así: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Configuración rápida de desarrollo - no adecuada para producción
# Ver https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# ADVERTENCIA DE SEGURIDAD: ¡mantenga la clave secreta usada en producción en secreto!
SECRET_KEY = 'django-insecure-dev-key-change-in-production'

# ADVERTENCIA DE SEGURIDAD: ¡no ejecute con debug activado en producción!
DEBUG = True

ALLOWED_HOSTS = []


# Definición de aplicaciones

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'csv_upload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'csv_validator_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'csv_validator_project.wsgi.application'


# Internacionalización
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'

# Archivos multimedia
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Configuración de carga de archivos
FILE_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760  # 10MB

