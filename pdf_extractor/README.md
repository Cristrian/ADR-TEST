# PDF Extractor - Extractor de CUFE

Este script procesa archivos PDF para extraer el CUFE (Código Único de Factura Electrónica) utilizando expresiones regulares y guarda los resultados en una base de datos SQLite.

## Requisitos

- Python >= 3.10
- pymupdf >= 1.26.7

## Instalación

1. Se requiere tener Python 3.10 o superior instalado:
```bash
python --version
```

2. Se instala directamente pymupdf:
```bash
pip install pymupdf>=1.26.7
```

## Estructura del Proyecto

```
pdf_extractor/
├── main.py              # Script principal
├── pdf_files/           # Carpeta donde se colocan los archivos PDF a procesar
├── cufe_facturas.db        # Base de datos SQLite (se crea automáticamente)
├── pyproject.toml       # Configuración del proyecto
└── README.md            # Este archivo
```

## Uso

### Preparar los archivos PDF

1. Se colocan los archivos PDF a procesar en la carpeta `pdf_files/`.
Para hacerlo por comando se puede ejecutar lo siguiente:
```bash
mkdir -p pdf_files
# Copiar los archivos PDF a esta carpeta
cp /ruta/a/tus/archivos/*.PDF pdf_files/
```

### Ejecutar el script

Se ejecuta el script principal:
```bash
python main.py
```

El script:
- Procesará todos los archivos PDF en la carpeta `pdf_files/`
- Buscará el CUFE en cada PDF (código hexadecimal de 95-100 caracteres)
- Mostrará los resultados en la consola
- Guardará los datos en la base de datos `cufe_facturas.db`

### Salida

El script mostrará en la consola:
- El resultado del procesamiento de cada archivo (número de páginas, tamaño, nombre y CUFE)
- Un mensaje cuando se guarde cada registro en la base de datos
- Un mensaje final cuando se complete el procesamiento

Ejemplo de salida:
```
Match encontrado en la página 1
{'num_pages': 2, 'file_size': 123456, 'file_name': 'factura.PDF', 'cufe': '49cf07e263e05b7e13adce4d8450b751dd45cd561aea9a8934198e8e391fa5f9916787641a4ece73d062e2c4dc5fded5'}
Datos guardados en cufe_facturas.db
Procesamiento completado
```

## Base de Datos

Los resultados se guardan en la base de datos SQLite `cufe_facturas.db` con la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Clave primaria autoincremental |
| file_name | TEXT | Nombre del archivo PDF |
| num_pages | INTEGER | Número de páginas del PDF |
| file_size | INTEGER | Tamaño del archivo en bytes |
| cufe | TEXT | CUFE extraído (puede ser NULL si no se encuentra) |
| processed_at | TIMESTAMP | Fecha y hora del procesamiento |

### Consultar la base de datos

Se pueden consultar los resultados usando SQLite:

```bash
sqlite3 cufe_facturas.db
```

Ejemplos de consultas:
```sql
-- Ver todos los registros
SELECT * FROM cufe_facturas;

-- Ver solo los archivos con CUFE encontrado
SELECT file_name, cufe FROM cufe_facturas WHERE cufe IS NOT NULL;

-- Contar archivos procesados
SELECT COUNT(*) FROM cufe_facturas;
```

## Funcionalidad

El script busca en cada PDF una expresión regular que coincide con:
- Un código hexadecimal de 95 a 100 caracteres
- Puede contener saltos de línea que son eliminados automáticamente
- Se detiene al encontrar el primer match en cada PDF

## Notas

- Si un PDF no contiene un CUFE válido, el campo `cufe` será `NULL` en la base de datos
- El script procesa todos los archivos en la carpeta `pdf_files/` automáticamente
- La base de datos se crea automáticamente si no existe
- Los registros se agregan a la base de datos sin eliminar los anteriores

