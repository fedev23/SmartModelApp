import os 
import shutil


def obtener_opciones_versiones(versiones, id, name):
    """
    Función que devuelve un diccionario con todas las versiones para el selector.

    Args:
    - versiones (list): Lista de diccionarios con las versiones.
    - id (str): Clave para obtener el ID de cada versión.
    - name (str): Clave para obtener el nombre de cada versión.

    Returns:
    - dict: Diccionario con las opciones para el selector.
    """
    if versiones:
        return {str(version[id]): version[name] for version in versiones}
    else:
        return {"": "No hay versiones"}, False

def obtener_ultimo_id_version(versiones, id):
    """
    Función que devuelve el ID de la última versión.

    Args:
    - versiones (list): Lista de diccionarios con las versiones.
    - id (str): Clave para obtener el ID de cada versión.

    Returns:
    - str: El ID de la última versión como valor predeterminado.
    """
    if versiones:
        return str(versiones[-1][id])
    else:
        return ""


def obtener_ultimo_nombre_archivo(versiones):
    """
    Función que devuelve el nombre del archivo del último valor en la lista de versiones.
    
    Args:
    - versiones (list): Lista de diccionarios con la información de los archivos.
    
    Returns:
    - str: El nombre del último archivo, si existe; si la lista está vacía, retorna una cadena vacía.
    """
    if versiones:
        # Accede al último diccionario y obtiene el valor de la clave 'nombre_archivo'
        return str(versiones[-1].get('nombre_archivo', ''))
    else:
        return ""
    
    

def copiar_json_si_existe(origen: str, destino: str, nombre_archivo: str = "Control de SmartModelStudio.json"):
    """
    Verifica si un archivo JSON existe en la carpeta de origen y lo copia a la carpeta de destino.
    
    Si la carpeta de destino no existe, no la creará, y si el archivo no se encuentra en la carpeta de origen,
    no realizará ninguna acción y devolverá un mensaje de error.
    
    :param origen: Ruta de la carpeta donde se buscará el archivo.
    :param destino: Ruta de la carpeta donde se copiará el archivo.
    :param nombre_archivo: Nombre del archivo JSON a verificar (por defecto es "Control de SmartModelStudio.json").
    :return: True si el archivo fue copiado correctamente, False si no se encontró el archivo.
    """
    archivo_origen = os.path.join(origen, nombre_archivo)
    
    # Verificar si el archivo existe en el origen
    if os.path.exists(archivo_origen):
        archivo_destino = os.path.join(destino, nombre_archivo)
        
        # Verificar si la carpeta destino existe. Si no, no se hará nada.
        if not os.path.exists(destino):
            print(f"Error: La carpeta de destino '{destino}' no existe.")
            return False
        
        # Copiar el archivo al destino
        shutil.copy(archivo_origen, archivo_destino)
        print(f"El archivo '{nombre_archivo}' se ha copiado a '{destino}'.")
        return True
    else:
        # Si el archivo no existe, mostrar el mensaje de error
        print(f"Error: El archivo '{nombre_archivo}' no existe en '{origen}'.")
        return False