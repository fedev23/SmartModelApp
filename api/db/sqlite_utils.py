import sqlite3
from datetime import datetime

def actualizar_ultimo_seleccionado_version(base_datos, tabla, id_columna, id_seleccionado, project_id):
    """
    Marca un registro como seleccionado para un project_id específico en la tabla y devuelve el ID seleccionado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param id_columna: Nombre de la columna que contiene los IDs de los registros.
    :param id_seleccionado: ID del registro que se desea marcar como seleccionado.
    :param project_id: ID del proyecto para filtrar los registros.
    :return: ID del registro recién marcado como seleccionado, o None si falla.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Resetear solo los registros del project_id especificado
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 0 WHERE project_id = ?", (project_id,))

        # Marcar el registro seleccionado para el project_id
        cursor.execute(
            f"UPDATE {tabla} SET is_last_selected = 1 WHERE {id_columna} = ? AND project_id = ?",
            (id_seleccionado, project_id)
        )

        # Confirmar los cambios
        conn.commit()

        # Devolver el ID marcado como seleccionado para el project_id
        cursor.execute(
            f"SELECT {id_columna} FROM {tabla} WHERE is_last_selected = 1 AND project_id = ?",
            (project_id,)
        )
        result = cursor.fetchone()

        if result:
            return result[0]  # Retorna el ID del registro seleccionado
        else:
            return None  # Si no se encuentra, devuelve None
    except sqlite3.Error as e:
        print(f"Error al actualizar el último seleccionado: {e}")
        return None
    finally:
        conn.close()        
        
def actualizar_ultimo_seleccionado_new(base_datos, tabla, id_columna, id_seleccionado, version_id):
    """
    Marca un registro como seleccionado en la tabla especificada, asegurando que 
    solo se afecten los registros vinculados al version_id correspondiente.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param id_columna: Nombre de la columna que contiene los IDs de los registros (id_jsons).
    :param id_seleccionado: ID del registro que se desea marcar como seleccionado.
    :param version_id: ID de la versión a la que pertenece el registro.
    :return: ID del registro recién marcado como seleccionado.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Resetear la selección solo en los registros que pertenezcan a la misma version_id
        cursor.execute(f"""
            UPDATE {tabla} 
            SET is_last_selected = 0 
            WHERE version_id = ?
        """, (version_id,))

        # Marcar el registro seleccionado dentro de la misma version_id
        cursor.execute(f"""
            UPDATE {tabla} 
            SET is_last_selected = 1 
            WHERE {id_columna} = ? AND version_id = ?
        """, (id_seleccionado, version_id))

        # Confirmar los cambios
        conn.commit()

        # Devolver el ID marcado como seleccionado
        cursor.execute(f"""
            SELECT {id_columna} FROM {tabla} 
            WHERE is_last_selected = 1 AND version_id = ?
        """, (version_id,))
        result = cursor.fetchone()

        if result:
            print(f"✅ Último ID seleccionado actualizado en version_id {version_id}: {result[0]}")
            return result[0]  # Retorna el ID del registro seleccionado
        else:
            print(f"⚠️ No se encontró un ID seleccionado para version_id {version_id}")
            return None  # Si no se encuentra, devuelve None
    except sqlite3.Error as e:
        print(f"❌ Error al actualizar el último seleccionado: {e}")
        return None
    finally:
        conn.close()
        
        
def obtener_ultimo_id_seleccionado(base_datos, tabla, column_id, project_id):
    """
    Obtiene el ID del último registro marcado como seleccionado para un project_id específico.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla.
    :param column_id: Nombre de la columna del ID en la tabla.
    :param project_id: ID del proyecto para filtrar los registros.
    :return: ID del último registro seleccionado, o None si no existe.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Consultar el ID del último seleccionado filtrado por project_id
        query = f"""
            SELECT {column_id} 
            FROM {tabla} 
            WHERE is_last_selected = 1 AND project_id = ? 
            LIMIT 1
        """
        cursor.execute(query, (project_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error al obtener el último ID seleccionado: {e}")
        return None
    finally:
        conn.close()



def obtener_ultimo_id_seleccionado_proyect(base_datos, tabla, column_id, user_id):
    """
    Obtiene el ID del último registro marcado como seleccionado para un user_id específico.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla.
    :param column_id: Nombre de la columna del ID en la tabla.
    :param user_id: ID del usuario para filtrar los registros.
    :return: ID del último registro seleccionado para el user_id, o None si no existe.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Consultar el ID del último seleccionado para el user_id especificado
        query = f"""
            SELECT {column_id} 
            FROM {tabla} 
            WHERE user_id = ? AND is_last_selected = 1 
            ORDER BY ROWID DESC 
            LIMIT 1
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        print(f"Error al obtener el último ID seleccionado: {e}")
        return None
    finally:
        conn.close()


def actualizar_ultimo_seleccionado_proyecto(base_datos, tabla, id_columna, id_seleccionado, user_id):
    """
    Marca un registro como seleccionado para un user_id específico en la tabla y devuelve el ID seleccionado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param id_columna: Nombre de la columna que contiene los IDs de los registros.
    :param id_seleccionado: ID del registro que se desea marcar como seleccionado.
    :param user_id: ID del usuario para filtrar los registros.
    :return: ID del registro recién marcado como seleccionado, o None si falla.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Resetear solo los registros del user_id especificado
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 0 WHERE user_id = ?", (user_id,))

        # Marcar el registro seleccionado para el user_id
        cursor.execute(
            f"UPDATE {tabla} SET is_last_selected = 1 WHERE {id_columna} = ? AND user_id = ?",
            (id_seleccionado, user_id)
        )

        # Confirmar los cambios
        conn.commit()

        # Devolver el ID marcado como seleccionado para el user_id
        cursor.execute(
            f"SELECT {id_columna} FROM {tabla} WHERE is_last_selected = 1 AND user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()

        if result:
            return result[0]  # Retorna el ID del registro seleccionado
        else:
            return None  # Si no se encuentra, devuelve None
    except sqlite3.Error as e:
        print(f"Error al actualizar el último seleccionado: {e}")
        return None
    finally:
        conn.close()
        
def obtener_ultimo_seleccionado(base_datos, tabla, columna_retorno):
    """
    Obtiene el valor de la columna especificada para el registro marcado como último seleccionado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param columna_retorno: Nombre de la columna cuyo valor se desea obtener.
    :return: Valor de la columna especificada o None si no hay registros seleccionados.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Obtener el valor del último seleccionado
        cursor.execute(f"SELECT {columna_retorno} FROM {tabla} WHERE is_last_selected = 1")
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Error al obtener el último seleccionado: {e}")
        return None
    finally:
        conn.close()



def obtener_ultimo_seleccionado_versiones(base_datos, tabla, columna_retorno, project_id):
    """
    Obtiene el valor de la columna especificada para el registro marcado como último seleccionado,
    filtrado por project_id.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param columna_retorno: Nombre de la columna cuyo valor se desea obtener.
    :param project_id: ID del proyecto para filtrar los registros.
    :return: Valor de la columna especificada o None si no hay registros seleccionados.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Obtener el valor del último seleccionado filtrado por project_id
        query = f"""
            SELECT {columna_retorno} 
            FROM {tabla} 
            WHERE is_last_selected = 1 AND project_id = ?
        """
        cursor.execute(query, (project_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Error al obtener el último seleccionado: {e}")
        return None
    finally:
        conn.close()        

def obtener_ultimo_seleccionado_proyecto(base_datos, tabla, columna_retorno, user_id):
    """
    Obtiene el valor de la columna especificada para el registro marcado como último seleccionado,
    filtrado por user_id.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param columna_retorno: Nombre de la columna cuyo valor se desea obtener.
    :param user_id: ID del usuario para filtrar los registros.
    :return: Valor de la columna especificada o None si no hay registros seleccionados.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Obtener el valor del último seleccionado filtrado por user_id
        query = f"""
            SELECT {columna_retorno} 
            FROM {tabla} 
            WHERE is_last_selected = 1 AND user_id = ?
        """
        cursor.execute(query, (user_id,))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"Error al obtener el último seleccionado: {e}")
        return None
    finally:
        conn.close()
        

def actualizar_ultimo_seleccionado(base_datos, tabla, id_columna, id_seleccionado):
    """
    Marca un registro como seleccionado en la tabla especificada y devuelve el ID seleccionado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param id_columna: Nombre de la columna que contiene los IDs de los registros.
    :param id_seleccionado: ID del registro que se desea marcar como seleccionado.
    :return: ID del registro recién marcado como seleccionado.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Resetear todos los registros
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 0")

        # Marcar el registro seleccionado
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 1 WHERE {id_columna} = ?", (id_seleccionado,))

        # Confirmar los cambios
        conn.commit()

        # Devolver el ID marcado como seleccionado
        cursor.execute(f"SELECT {id_columna} FROM {tabla} WHERE is_last_selected = 1")
        result = cursor.fetchone()

        if result:
            return result[0]  # Retorna el ID del registro seleccionado
        else:
            return None  # Si no se encuentra, devuelve None
    except sqlite3.Error as e:
        print(f"Error al actualizar el último seleccionado: {e}")
        return None
    finally:
        conn.close()

##ESTE ES EL NUEVO EDITADO
def obtener_ultimo_id_seleccionado_edited(base_datos, tabla, column_id, version_id):
    """
    Obtiene el ID del último registro marcado como seleccionado dentro de una version_id dada.
    Si no hay un registro seleccionado, obtiene el último id_jsons asociado a esa version_id.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla.
    :param column_id: Nombre de la columna del ID en la tabla.
    :param version_id: ID de la versión para filtrar.
    :return: ID del último registro seleccionado para esa version_id o el último id_jsons si no hay seleccionado.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Buscar el último ID seleccionado dentro de la version_id dada
        query = f"""
            SELECT {column_id} FROM {tabla} 
            WHERE is_last_selected = 1 AND version_id = ? 
            LIMIT 1
        """
        cursor.execute(query, (version_id,))
        result = cursor.fetchone()

        if result:
            print(f"✅ Último ID seleccionado dentro de version_id {version_id}: {result[0]}")
            return result[0]  # Devuelve el ID si hay un registro seleccionado
        
        # Si no hay un seleccionado, obtener el último id_jsons registrado dentro de esa version_id
        print(f"⚠️ No hay un ID seleccionado, obteniendo el último id_jsons para version_id {version_id}...")
        ultimo_id = obtener_ultimo_id_json_por_version(base_datos, tabla, column_id, version_id)
        print(ultimo_id)
        if ultimo_id:
            print(f"✅ Último id_jsons registrado para version_id {version_id}: {ultimo_id}")
        
        return ultimo_id if ultimo_id else None

    except sqlite3.Error as e:
        print(f"❌ Error al obtener el último ID seleccionado para version_id {version_id}: {e}")
        return None
    finally:
        conn.close()

def obtener_ultimo_id_json_por_version(base_datos, tabla, columna_retorno, version_id):
    """
    Obtiene el último id_jsons insertado en la tabla, asociado al version_id dado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param columna_retorno: Nombre de la columna cuyo valor se desea obtener (id_jsons).
    :param version_id: ID de la versión para filtrar los registros.
    :return: Último id_jsons asociado a la version_id dada o None si no hay registros.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Obtener el último id_jsons basado en la versión_id (ordenado por id_jsons DESC)
        cursor.execute(f"""
            SELECT {columna_retorno} FROM {tabla} 
            WHERE version_id = ? 
            ORDER BY id_jsons DESC 
            LIMIT 1
        """, (version_id,))

        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    except sqlite3.Error as e:
        print(f"Error al obtener el último id_jsons por version_id: {e}")
        return None
    finally:
        conn.close()


                
def actualizar_ultimo_seleccionado_update(base_datos, tabla, columna_id, nuevo_id):
    """
    Actualiza la base de datos para marcar un nuevo ID como el último seleccionado.
    
    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla en la que se realizará la operación.
    :param columna_id: Nombre de la columna que contiene los IDs.
    :param nuevo_id: ID que se marcará como seleccionado.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        # Limpiar la selección previa
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 0")

        # Marcar el nuevo ID como seleccionado
        cursor.execute(f"UPDATE {tabla} SET is_last_selected = 1 WHERE {columna_id} = ?", (nuevo_id,))
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al actualizar el último seleccionado: {e}")
    finally:
        conn.close()
        
def obtener_nombre_version_por_id_json(base_datos, tabla, id_jsons):
    """
    Obtiene el nombre de versión asociado a un id_jsons dado.

    :param base_datos: Ruta al archivo de base de datos SQLite.
    :param tabla: Nombre de la tabla.
    :param id_jsons: ID del JSON para obtener su versión.
    :return: Nombre de la versión o None si no existe.
    """
    conn = sqlite3.connect(base_datos)
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT nombre_version FROM {tabla} WHERE id_jsons = ?
        """, (id_jsons,))

        resultado = cursor.fetchone()
        return resultado[0] if resultado else None

    except sqlite3.Error as e:
        print(f"Error al obtener el nombre de la versión por id_jsons: {e}")
        return None
    finally:
        conn.close()



def obtener_ultimo_modelo_por_version(database_path, version_id):
    """
    Obtiene el último modelo ejecutado con su estado y fecha, dado el ID de versión.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param version_id: ID de la versión en la tabla model_execution.
    :return: Diccionario con 'model_name', 'execution_state', y 'execution_date', o valores predeterminados si no hay registros.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Ejecutar la consulta para obtener el último modelo
        query = '''
        SELECT model_name, execution_state, execution_date
        FROM model_execution
        WHERE version_id = ?
        ORDER BY datetime(execution_date) DESC, execution_id DESC
        LIMIT 1;
        '''
        cur.execute(query, (version_id,))

        # Recuperar el resultado
        result = cur.fetchone()

        if result:
            return {
                "model_name": result[0],
                "execution_state": result[1],
                "execution_date": result[2],
            }
        else:
            print(f"No se encontró ningún modelo para version_id={version_id}")
            return {
                "model_name": None,
                "execution_state": "No ejecutado",
                "execution_date": "No disponible",
            }

    except sqlite3.Error as e:
        print(f"Error al obtener el último modelo para version_id={version_id}: {e}")
        return {
            "model_name": None,
            "execution_state": "Error en base de datos",
            "execution_date": "Error",
        }
    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            conn.close()


def obtener_ultimo_modelo_por_version_json(database_path, json_version_id):
    """
    Obtiene el último modelo ejecutado con su estado, fecha y mensaje de error si hubo un fallo.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param json_version_id: ID de la versión JSON en la tabla model_execution (entero o convertible a entero).
    :return: Diccionario con 'model_name', 'execution_state', 'execution_date' y 'mensaje_error' (si hubo error).
    """
    conn = None  # Inicializar conn para evitar errores en el finally
    try:
        # Validar y convertir json_version_id a entero
        print(f"Valor inicial de json_version_id: {json_version_id}")
        if json_version_id is None:
            raise ValueError("json_version_id es None, no es válido.")

        json_version_id = int(json_version_id)
        if json_version_id <= 0:
            raise ValueError(f"json_version_id no es un ID válido: {json_version_id}")

        print(f"json_version_id convertido: {json_version_id}")

        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Depuración: imprimir el ID buscado
        print(f"Buscando modelos para json_version_id={json_version_id}")

        # Ejecutar la consulta para obtener el último modelo
        query = '''
        SELECT model_name, execution_state, execution_date
        FROM model_execution
        WHERE json_version_id = ?
        ORDER BY datetime(execution_date) DESC, execution_id DESC
        LIMIT 1;
        '''
        cur.execute(query, (json_version_id,))

        # Recuperar resultado
        result = cur.fetchone()
        print(f"Resultado de la consulta para json_version_id={json_version_id}: {result}")

        if result:
            model_name, execution_state, execution_date = result

            # Inicializar mensaje_error como None por defecto
            mensaje_error = None

            # Verificar si hubo error en execution_state y si existe la columna mensaje_error
            if "error" in execution_state.lower():
                cur.execute("PRAGMA table_info(model_execution)")
                columnas = [col[1] for col in cur.fetchall()]

                if "mensaje_error" in columnas:
                    cur.execute("""
                        SELECT mensaje_error FROM model_execution
                        WHERE json_version_id = ?
                        ORDER BY datetime(execution_date) DESC, execution_id DESC
                        LIMIT 1;
                    """, (json_version_id,))
                    mensaje_error_result = cur.fetchone()
                    mensaje_error = mensaje_error_result[0] if mensaje_error_result else None

            return {
                "model_name": model_name,
                "execution_state": execution_state,
                "execution_date": execution_date,
                "mensaje_error": mensaje_error  # Devuelve None si no hay error
            }
        else:
            print(f"No se encontró ningún modelo para json_version_id={json_version_id}")
            return {
                "model_name": None,
                "execution_state": "No ejecutado",
                "execution_date": "No disponible",
                "mensaje_error": None  # Asegurar que no quede un error antiguo
            }

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        return {
            "model_name": None,
            "execution_state": "ID inválido",
            "execution_date": "No disponible",
            "mensaje_error": None  # Evita arrastrar errores previos
        }

    except sqlite3.Error as e:
        print(f"Error al obtener el último modelo para json_version_id={json_version_id}: {e}")
        return {
            "model_name": None,
            "execution_state": "Error en base de datos",
            "execution_date": "Error",
            "mensaje_error": None  # Asegurar que no quede un error previo
        }

    finally:
        # Cerrar la conexión si se creó
        if conn:
            conn.close()


def obtener_ultimo_modelo_por_version_y_nombre(database_path, nombre_modelo, version_id=None, json_version_id=None):
    """
    Obtiene el último modelo ejecutado con su estado y fecha, dado un nombre específico, 
    buscando por version_id si se proporciona, o por json_version_id en caso contrario.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param nombre_modelo: Nombre del modelo a filtrar.
    :param version_id: (Opcional) ID de la versión en la tabla model_execution.
    :param json_version_id: (Opcional) ID del JSON de la versión.
    :return: Diccionario con 'model_name', 'execution_state', y 'execution_date', o valores predeterminados si no hay registros.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Determinar la consulta y los parámetros según los argumentos proporcionados
        if version_id is not None:
            query = '''
            SELECT model_name, execution_state, execution_date
            FROM model_execution
            WHERE version_id = ? AND model_name = ?
            ORDER BY datetime(execution_date) DESC, execution_id DESC
            LIMIT 1;
            '''
            params = (version_id, nombre_modelo)
        elif json_version_id is not None:
            query = '''
            SELECT model_name, execution_state, execution_date
            FROM model_execution
            WHERE json_version_id = ? AND model_name = ?
            ORDER BY datetime(execution_date) DESC, execution_id DESC
            LIMIT 1;
            '''
            params = (json_version_id, nombre_modelo)
        else:
            raise ValueError("Debe proporcionarse al menos version_id o json_version_id.")

        # Ejecutar la consulta
        cur.execute(query, params)
        result = cur.fetchone()

        if result:
            return {
                "model_name": result[0],
                "execution_state": result[1],
                "execution_date": result[2],
            }
        else:
            print(f"No se encontró ningún modelo para los criterios especificados.")
            return {
                "model_name": None,
                "execution_state": "No ejecutado",
                "execution_date": "No disponible",
            }

    except sqlite3.Error as e:
        print(f"Error al obtener el último modelo: {e}")
        return {
            "model_name": None,
            "execution_state": "Error en base de datos",
            "execution_date": "Error",
        }
    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            conn.close()



def obtener_ultimo_modelo_por_version_y_nombre(database_path, version_id, nombre_modelo):
    """
    Obtiene el último modelo ejecutado con su estado, fecha y mensaje de error si hubo un fallo.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param version_id: ID de la versión en la tabla model_execution.
    :param nombre_modelo: Nombre del modelo a filtrar.
    :return: Diccionario con 'model_name', 'execution_state', 'execution_date' y 'mensaje_error' (si hubo error).
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        print(f"El ID de la versión es: {version_id}")

        # Ejecutar la consulta base para obtener model_name, execution_state y execution_date
        query = '''
        SELECT model_name, execution_state, execution_date
        FROM model_execution
        WHERE version_id = ? AND model_name = ?
        ORDER BY datetime(execution_date) DESC, execution_id DESC
        LIMIT 1;
        '''
        cur.execute(query, (version_id, nombre_modelo))

        # Recuperar el resultado
        result = cur.fetchone()

        if result:
            model_name, execution_state, execution_date = result

            # Verificar si el estado indica error
            mensaje_error = None
            if "error" in execution_state.lower():  # Si hay error, recuperar mensaje_error
                cur.execute("PRAGMA table_info(model_execution)")
                columnas = [col[1] for col in cur.fetchall()]

                if "mensaje_error" in columnas:
                    cur.execute("""
                        SELECT mensaje_error FROM model_execution
                        WHERE version_id = ? AND model_name = ?
                        ORDER BY datetime(execution_date) DESC, execution_id DESC
                        LIMIT 1;
                    """, (version_id, nombre_modelo))
                    mensaje_error = cur.fetchone()
                    mensaje_error = mensaje_error[0] if mensaje_error else None

            # Construir el resultado
            resultado = {
                "model_name": model_name,
                "execution_state": execution_state,
                "execution_date": execution_date,
            }
            if mensaje_error:
                resultado["mensaje_error"] = mensaje_error  # Solo se agrega si hubo error

            return resultado

        else:
            print(f"No se encontró ningún modelo para version_id={version_id} y model_name={nombre_modelo}")
            return {
                "model_name": None,
                "execution_state": "No ejecutado",
                "execution_date": "No disponible",
            }

    except sqlite3.Error as e:
        print(f"Error al obtener el último modelo para version_id={version_id} y model_name={nombre_modelo}: {e}")
        return {
            "model_name": None,
            "execution_state": "Error en base de datos",
            "execution_date": "Error",
        }
    finally:
        # Cerrar la conexión a la base de datos
        if conn:
            conn.close()
            
def obtener_ultimo_modelo_por_validacion_sc_y_nombre(database_path, id_validacion_sc=None, id_nombre_file=None, nombre_modelo=None):
    """
    Obtiene el último modelo ejecutado con su estado, fecha y mensaje de error si hubo un fallo.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param id_validacion_sc: (Opcional) ID de validación scoring en la tabla validation_scoring.
    :param id_nombre_file: (Opcional) ID del archivo en la tabla validation_scoring.
    :param nombre_modelo: (Opcional) Nombre del modelo a filtrar.
    :return: Diccionario con 'nombre_modelo', 'execution_state', 'fecha_de_ejecucion' y 'mensaje_error' si hubo error.
    """
    if not (id_validacion_sc or id_nombre_file):
        raise ValueError("Se debe proporcionar al menos 'id_validacion_sc' o 'id_nombre_file'.")

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Construir la consulta base para obtener nombre_modelo, execution_state y fecha_de_ejecucion
        query = '''
        SELECT nombre_modelo, execution_state, fecha_de_ejecucion
        FROM validation_scoring
        WHERE 1 = 1
        '''
        params = []

        # Agregar condiciones según los parámetros recibidos
        if id_validacion_sc is not None:
            query += " AND id_validacion_sc = ?"
            params.append(id_validacion_sc)

        if id_nombre_file is not None:
            query += " AND id_nombre_file = ?"
            params.append(id_nombre_file)

        if nombre_modelo is not None:
            query += " AND nombre_modelo = ?"
            params.append(nombre_modelo)

        # Ordenar para obtener el modelo más reciente
        query += " ORDER BY datetime(fecha_de_ejecucion) DESC, id_validacion_sc DESC LIMIT 1;"

        # Ejecutar la consulta
        cur.execute(query, tuple(params))
        result = cur.fetchone()

        if result:
            nombre_modelo, execution_state, fecha_de_ejecucion = result

            # Verificar si hubo error en execution_state
            mensaje_error = None
            if "error" in execution_state.lower():
                cur.execute("PRAGMA table_info(validation_scoring)")
                columnas = [col[1] for col in cur.fetchall()]

                if "mensaje_error" in columnas:
                    cur.execute("""
                        SELECT mensaje_error FROM validation_scoring
                        WHERE id_validacion_sc = ? AND nombre_modelo = ?
                        ORDER BY datetime(fecha_de_ejecucion) DESC, id_validacion_sc DESC
                        LIMIT 1;
                    """, (id_validacion_sc, nombre_modelo))
                    mensaje_error = cur.fetchone()
                    mensaje_error = mensaje_error[0] if mensaje_error else None

            # Construir el resultado
            resultado = {
                "nombre_modelo": nombre_modelo,
                "execution_state": execution_state,
                "fecha_de_ejecucion": fecha_de_ejecucion,
            }
            if mensaje_error:
                resultado["mensaje_error"] = mensaje_error  # Solo se agrega si hubo error

            return resultado

        else:
            print("No se encontró ningún modelo para los parámetros proporcionados.")
            return {
                "nombre_modelo": None,
                "execution_state": "No ejecutado",
                "fecha_de_ejecucion": "No disponible",
            }

    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return {
            "nombre_modelo": None,
            "execution_state": "Error en base de datos",
            "fecha_de_ejecucion": "Error",
        }
    finally:
        if conn:
            conn.close()
    
            

def obtener_ultimo_scoring_por_json_version_y_modelo(database_path, id_score=None, id_nombre_file=None, nombre_modelo=None):
    """
    Obtiene el último modelo ejecutado con su estado, fecha y mensaje de error si hubo un fallo.

    :param database_path: Ruta al archivo de la base de datos SQLite.
    :param id_score: (Opcional) ID de scoring en la tabla 'scoring'.
    :param id_nombre_file: (Opcional) ID del archivo en la tabla 'scoring'.
    :param nombre_modelo: (Opcional) Nombre del modelo a filtrar.
    :return: Diccionario con 'model_name', 'execution_state', 'execution_date' y 'mensaje_error' (si hubo error, sino None).
    """
    if not (id_score or id_nombre_file or nombre_modelo):
        raise ValueError("Se debe proporcionar al menos 'id_score', 'id_nombre_file' o 'nombre_modelo'.")

    conn = None
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect(database_path)
        cur = conn.cursor()

        # Construcción de la consulta base
        query = '''
        SELECT model_name, execution_state, fecha_de_ejecucion
        FROM scoring
        WHERE 1=1
        '''
        params = []

        # Agregar condiciones según los parámetros recibidos
        if id_score is not None:
            query += " AND id_score = ?"
            params.append(id_score)

        if id_nombre_file is not None:
            query += " AND id_nombre_file = ?"
            params.append(id_nombre_file)

        if nombre_modelo is not None:
            query += " AND model_name = ?"
            params.append(nombre_modelo)

        # Ordenar para obtener el modelo más reciente
        query += " ORDER BY datetime(fecha_de_ejecucion) DESC, id_score DESC LIMIT 1;"

        # Ejecutar la consulta
        cur.execute(query, tuple(params))
        result = cur.fetchone()

        if result:
            model_name, execution_state, execution_date = result

            # Inicializar mensaje_error como None por defecto
            mensaje_error = None

            # Verificar si hubo error en execution_state y si existe la columna mensaje_error
            if "error" in execution_state.lower():
                cur.execute("PRAGMA table_info(scoring)")
                columnas = [col[1] for col in cur.fetchall()]

                if "mensaje_error" in columnas:
                    cur.execute("""
                        SELECT mensaje_error FROM scoring
                        WHERE model_name = ? AND execution_state = ?
                        ORDER BY datetime(fecha_de_ejecucion) DESC, id_score DESC LIMIT 1;
                    """, (model_name, execution_state))
                    mensaje_error_result = cur.fetchone()
                    mensaje_error = mensaje_error_result[0] if mensaje_error_result else None

            return {
                "model_name": model_name,
                "execution_state": execution_state,
                "execution_date": execution_date,
                "mensaje_error": mensaje_error  # Será None si no hay error
            }

        else:
            print("No se encontró ningún modelo con los parámetros proporcionados.")
            return {
                "model_name": None,
                "execution_state": "No ejecutado",
                "execution_date": "No disponible",
                "mensaje_error": None  # Asegurar que no quede un error antiguo
            }

    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return {
            "model_name": None,
            "execution_state": "Error en base de datos",
            "execution_date": "Error",
            "mensaje_error": None  # También limpiar en caso de error
        }

    finally:
        if conn:
            conn.close()
