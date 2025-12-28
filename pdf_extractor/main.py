import os
import re
import sqlite3
import pymupdf

def process_pdf(pdf_path):
    # Abrimos el archivo PDF
    doc = pymupdf.open(pdf_path)
    # Obtenemos el número de páginas
    num_pages = len(doc)
    # Obtenemos el tamaño del archivo en bytes
    file_size = os.path.getsize(pdf_path)
    # Obtenemos el nombre del archivo
    file_name = os.path.basename(pdf_path)

    # Extraemos el texto de las páginas buscando las siguiente expresion regular:
    # (\b([0-9a-fA-F]\n*){95,100}\b) -> Esto es un grupo de 95 a 100 caracteres hexadecimales
    
    cufe = None
    for page in doc:
        text = page.get_text()
        match = re.search(r'\b([0-9a-fA-F]\n*){95,100}\b', text)
        if match:
            # Obtenemos el match completo y eliminamos los saltos de línea
            cufe = match.group(0).replace('\n', '')
            print(f"Match encontrado en la página {page.number + 1}")
            break  # Al encontrar el CUFE, salimos del bucle
    
    return {
        "num_pages": num_pages,
        "file_size": file_size,
        "file_name": file_name,
        "cufe": cufe
    }


def save_to_sqlite(result, db_path="cufe_facturas.db"):
    """
    Guarda el resultado del procesamiento del PDF en una base de datos SQLite.
    
    Args:
        result: Diccionario con los datos a guardar (num_pages, file_size, file_name, cufe)
        db_path: Ruta al archivo de base de datos SQLite (por defecto: pdf_extractor.db)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Creamos la tabla si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cufe_facturas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            num_pages INTEGER,
            file_size INTEGER,
            cufe TEXT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insertamos los datos
    cursor.execute('''
        INSERT INTO cufe_facturas (file_name, num_pages, file_size, cufe)
        VALUES (?, ?, ?, ?)
    ''', (
        result["file_name"],
        result["num_pages"],
        result["file_size"],
        result["cufe"]
    ))
    
    conn.commit()
    conn.close()
    print(f"Datos guardados en la base de datos {db_path}")


def main():
    # Obtenemos la lista de archivos PDF en la carpeta pdf_files
    pdf_files = os.listdir("pdf_files")
    for pdf_file in pdf_files:
        pdf_path = os.path.join("pdf_files", pdf_file)
        result = process_pdf(pdf_path)
        print(result)
        save_to_sqlite(result)
    
    print("Procesamiento completado")




if __name__ == "__main__":
    main()
