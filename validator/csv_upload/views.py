from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv
import io
import re


def upload_csv(request):
    """Página principal para carga de CSV."""
    return render(request, 'csv_upload/upload.html')


def validate_column1(value):
    """Validar Columna 1: Solo números enteros entre 3 y 10 caracteres."""
    value = str(value).strip()
    if not value.isdigit():
        return False, 'debe contener solo números enteros'
    if len(value) < 3 or len(value) > 10:
        return False, f'debe tener entre 3 y 10 caracteres (tiene {len(value)})'
    return True, None


def validate_column2(value):
    """Validar Columna 2: Solo correos electrónicos."""
    value = str(value).strip()
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, value):
        return False, 'debe ser un correo electrónico válido'
    return True, None


def validate_column3(value):
    """Validar Columna 3: Solo valores "CC" o "TI"."""
    value = str(value).strip()
    if value not in ['CC', 'TI']:
        return False, 'debe ser "CC" o "TI"'
    return True, None


def validate_column4(value):
    """Validar Columna 4: Valores entre 500000 y 1500000."""
    try:
        num_value = float(value)
        if num_value < 500000 or num_value > 1500000:
            return False, f'debe estar entre 500000 y 1500000'
        return True, None
    except (ValueError, TypeError):
        return False, 'debe ser un número válido'


@csrf_exempt
def verify_csv(request):
    """Verificar la estructura del archivo CSV cargado."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Solo se permite el método POST'}, status=405)
    
    if 'csv_file' not in request.FILES:
        return JsonResponse({'error': 'No se proporcionó archivo CSV'}, status=400)
    
    csv_file = request.FILES['csv_file']
    
    try:
        # Leer el archivo CSV
        file_content = csv_file.read().decode('utf-8')
        csv_reader = csv.reader(io.StringIO(file_content))
        
        # Leer todas las filas como datos (sin encabezado)
        data_rows = list(csv_reader)
        row_count = len(data_rows)
        
        # Verificar si el archivo tiene filas de datos
        if row_count == 0:
            return JsonResponse({
                'valid': False,
                'error': 'El archivo está vacío'
            })
        
        # Recopilar todos los errores sin detenerse en el primero
        all_errors = []
        expected_columns = 5
        
        # Validar cada fila
        for idx, row in enumerate(data_rows, start=1):
            row_errors = []
            
            # Verificar si la fila está vacía
            if not row or len(row) == 0:
                all_errors.append({
                    'row': idx,
                    'column': None,
                    'value': '',
                    'error': 'La fila está vacía'
                })
                continue
            
            # Verificar número de columnas
            actual_columns = len(row)
            if actual_columns != expected_columns:
                all_errors.append({
                    'row': idx,
                    'column': None,
                    'value': f'{actual_columns} columnas',
                    'error': f'Debe tener exactamente {expected_columns} columnas (tiene {actual_columns})'
                })
            
            # Asegurar que la fila tenga al menos 5 columnas para validar (rellenar con vacío si es necesario)
            while len(row) < 5:
                row.append('')
            
            # Validar Columna 1: Números enteros entre 3 y 10 caracteres
            if len(row) > 0 and row[0]:
                is_valid, error_msg = validate_column1(row[0])
                if not is_valid:
                    all_errors.append({
                        'row': idx,
                        'column': 1,
                        'value': row[0],
                        'error': f'Columna 1: {error_msg}'
                    })
            elif len(row) > 0:
                all_errors.append({
                    'row': idx,
                    'column': 1,
                    'value': '',
                    'error': 'Columna 1: está vacía'
                })
            
            # Validar Columna 2: Correo electrónico
            if len(row) > 1 and row[1]:
                is_valid, error_msg = validate_column2(row[1])
                if not is_valid:
                    all_errors.append({
                        'row': idx,
                        'column': 2,
                        'value': row[1],
                        'error': f'Columna 2: {error_msg}'
                    })
            elif len(row) > 1:
                all_errors.append({
                    'row': idx,
                    'column': 2,
                    'value': '',
                    'error': 'Columna 2: está vacía'
                })
            
            # Validar Columna 3: Solo "CC" o "TI"
            if len(row) > 2 and row[2]:
                is_valid, error_msg = validate_column3(row[2])
                if not is_valid:
                    all_errors.append({
                        'row': idx,
                        'column': 3,
                        'value': row[2],
                        'error': f'Columna 3: {error_msg}'
                    })
            elif len(row) > 2:
                all_errors.append({
                    'row': idx,
                    'column': 3,
                    'value': '',
                    'error': 'Columna 3: está vacía'
                })
            
            # Validar Columna 4: Valores entre 500000 y 1500000
            if len(row) > 3 and row[3]:
                is_valid, error_msg = validate_column4(row[3])
                if not is_valid:
                    all_errors.append({
                        'row': idx,
                        'column': 4,
                        'value': row[3],
                        'error': f'Columna 4: {error_msg}'
                    })
            elif len(row) > 3:
                all_errors.append({
                    'row': idx,
                    'column': 4,
                    'value': '',
                    'error': 'Columna 4: está vacía'
                })
            
            # Columna 5: Permite cualquier valor (no se valida)
        
        if all_errors:
            return JsonResponse({
                'valid': False,
                'error': 'El archivo contiene errores de validación',
                'details': {
                    'validation_errors': all_errors[:50]  # Limitar a las primeras 50
                }
            })
        
        # Si todas las verificaciones pasan
        return JsonResponse({
            'valid': True,
            'message': 'La estructura del archivo es válida',
            'details': {
                'columns': expected_columns,
                'rows': row_count
            }
        })
        
    except UnicodeDecodeError:
        return JsonResponse({
            'valid': False,
            'error': 'El archivo CSV debe estar codificado en UTF-8'
        })
    except Exception as e:
        return JsonResponse({
            'valid': False,
            'error': f'Error al leer el archivo CSV: {str(e)}'
        })

