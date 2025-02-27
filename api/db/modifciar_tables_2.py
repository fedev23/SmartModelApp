import sqlite3
from datetime import datetime

def actualizar_ultimo_file_en_tabla(tabla, pk, campo_file, campo_version):
    """
    Abre la conexión a "Modeling_App.db", agrega la columna 'ultimo_file_usado'
    (si no existe) y, para cada valor de {campo_version} (ej. json_versiones_id), 
    actualiza el registro con mayor {campo_file} a 1 y el resto a 0.
    
    Parámetros:
      - tabla: nombre de la tabla.
      - pk: nombre de la llave primaria.
      - campo_file: nombre del campo que identifica el file (ej. 'id_nombre_file').
      - campo_version: nombre del campo de versión (ej. 'json_versiones_id').
    """
    conn = sqlite3.connect("Modeling_App.db")
    cursor = conn.cursor()
    
    # Verificar si la columna 'ultimo_file_usado' existe en la tabla
    cursor.execute(f"PRAGMA table_info({tabla})")
    columnas = cursor.fetchall()
    nombres_columnas = [col[1] for col in columnas]
    
    if 'ultimo_file_usado' not in nombres_columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN ultimo_file_usado INTEGER DEFAULT 0")
        conn.commit()
        print(f"Columna 'ultimo_file_usado' agregada a la tabla {tabla}.")
    else:
        print(f"La columna 'ultimo_file_usado' ya existe en la tabla {tabla}.")
    
    # Reinicializar la columna para todos los registros
    cursor.execute(f"UPDATE {tabla} SET ultimo_file_usado = 0")
    conn.commit()
    
    # Para cada valor distinto de {campo_version}, se marca el registro con mayor {campo_file} en 1.
    cursor.execute(f"SELECT DISTINCT {campo_version} FROM {tabla}")
    versiones = cursor.fetchall()
    
    for (version,) in versiones:
        query = f"""
            SELECT {pk}, {campo_file}
            FROM {tabla}
            WHERE {campo_version} = ?
            ORDER BY {campo_file} DESC
            LIMIT 1
        """
        cursor.execute(query, (version,))
        resultado = cursor.fetchone()
        if resultado:
            pk_valor, _ = resultado
            cursor.execute(f"UPDATE {tabla} SET ultimo_file_usado = 1 WHERE {pk} = ?", (pk_valor,))
    
    conn.commit()
    print(f"Se actualizó el campo 'ultimo_file_usado' en la tabla {tabla}.")
    conn.close()

def comparar_ultimo_file_usado(formato_fecha="%Y-%m-%d %H:%M:%S"):
    """
    Abre la conexión a "Modeling_App.db", extrae de ambas tablas (validation_scoring y scoring)
    el registro marcado con ultimo_file_usado = 1 y con la fecha_de_carga más reciente,
    y los compara para determinar cuál es el último file usado en tiempo.
    
    Se asume que la fecha está en formato 'YYYY-MM-DD HH:MM:SS'.
    """
    conn = sqlite3.connect("Modeling_App.db")
    cursor = conn.cursor()
    
    # Extraer de validation_scoring
    query_vs = """
        SELECT id_nombre_file, fecha_de_carga 
        FROM validation_scoring 
        WHERE ultimo_file_usado = 1 
        ORDER BY datetime(fecha_de_carga) DESC 
        LIMIT 1
    """
    cursor.execute(query_vs)
    vs_registro = cursor.fetchone()
    
    # Extraer de scoring
    query_sc = """
        SELECT id_nombre_file, fecha_de_carga 
        FROM scoring 
        WHERE ultimo_file_usado = 1 
        ORDER BY datetime(fecha_de_carga) DESC 
        LIMIT 1
    """
    cursor.execute(query_sc)
    sc_registro = cursor.fetchone()
    
    if not vs_registro or not sc_registro:
        print("No se encontraron registros marcados con ultimo_file_usado = 1 en una de las tablas.")
        conn.close()
        return None
    
    id_file_vs, fecha_vs = vs_registro
    id_file_sc, fecha_sc = sc_registro
    
    try:
        dt_vs = datetime.strptime(fecha_vs, formato_fecha)
    except Exception as e:
        print("Error al convertir fecha_de_carga de validation_scoring:", e)
        conn.close()
        return None
    
    try:
        dt_sc = datetime.strptime(fecha_sc, formato_fecha)
    except Exception as e:
        print("Error al convertir fecha_de_carga de scoring:", e)
        conn.close()
        return None
    
    conn.close()
    
    if dt_vs > dt_sc:
        print("El último file usado es de validation_scoring:", vs_registro)
        return ("validation_scoring", id_file_vs, fecha_vs)
    else:
        print("El último file usado es de scoring:", sc_registro)
        return ("scoring", id_file_sc, fecha_sc)

# Actualizar el campo 'ultimo_file_usado' en ambas tablas
actualizar_ultimo_file_en_tabla(
    tabla="validation_scoring",
    pk="id_validacion_sc",
    campo_file="id_nombre_file",
    campo_version="json_versiones_id"
)

actualizar_ultimo_file_en_tabla(
    tabla="scoring",
    pk="id_score",
    campo_file="id_nombre_file",
    campo_version="json_versiones_id"
)

   