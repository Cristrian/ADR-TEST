# Validador de Archivos CSV

Aplicación Django 6 para validar la estructura y contenido de archivos separados por comas.

## Requisitos

- Python 3.12 o superior
- Django 6.0 o superior
- uv (opcional, para gestión de dependencias)

## Instalación y Ejecución

1. **Instalar dependencias** (usando uv o pip):
   ```bash
   uv sync
   # o
   pip install django>=6.0
   ```

2. **Iniciar el servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

3. **Abrir el navegador y navegar a**:
   ```
   http://127.0.0.1:8000/
   ```

## Uso

1. Hacer clic en "Elegir Archivo CSV" o arrastrar y soltar un archivo
2. Hacer clic en el botón "Verificar Estructura del Archivo"
3. Revisar los resultados de la validación

## Reglas de Validación

El validador verifica que el archivo cumpla con las siguientes reglas:

### Estructura General
- El archivo debe tener **exactamente 5 columnas** en todas las filas
- El archivo **no requiere encabezado** (la primera fila se trata como datos)
- El archivo puede tener **cualquier extensión** (solo importa que esté separado por comas)
- El archivo debe estar codificado en **UTF-8**

### Validación por Columna

1. **Columna 1**: Solo números enteros entre 3 y 10 caracteres
2. **Columna 2**: Solo correos electrónicos válidos
3. **Columna 3**: Solo permite los valores "CC" o "TI"
4. **Columna 4**: Solo valores numéricos entre 500000 y 1500000
5. **Columna 5**: Permite cualquier valor (sin validación)

### Características

- Detecta **todos los errores** en el archivo, no solo el primero
- Muestra errores detallados indicando la fila, columna y el problema específico
- Interfaz web moderna y fácil de usar
- Validación en tiempo real sin necesidad de base de datos

## Estructura del Proyecto

```
validator/
├── manage.py
├── csv_validator_project/     # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── csv_upload/                # Aplicación Django
    ├── views.py               # Lógica de validación
    ├── urls.py                # URLs de la aplicación
    └── templates/
        └── csv_upload/
            └── upload.html    # Plantilla de la página principal
```
