from shiny import ui
from api.db.sqlite_utils import *
from funciones_modelo.help_models import *
import sqlite3

def create_modal_warning_exist_model(name, nombre_version, id_boton):
    return ui.modal(
        ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.div(
                        # Estilo para el texto de advertencia
                        ui.tags.p(
                            f"El modelo en la etapa '{name}' ya existe en la versión '{nombre_version}'. "
                            "Si usted quiere continuar, se le recomienda generar una nueva versión.",
                            style="color: #d9534f; font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 20px;"
                        ),
                        style="padding: 10px; border: 1px solid #d9534f; border-radius: 5px; background-color: #f2dede;"
                    )
                )
            )
        ),
        title=ui.tags.div(
            "⚠️ Advertencia",
            style="color: #f0ad4e; font-size: 20px; font-weight: bold; text-align: center;"
        ),
        easy_close=True,
        size='xs',
        footer=ui.row(
            # Primera fila de botones
            ui.column(
                5,
                ui.tags.div(
                    # Botón "Cancelar"
                    ui.input_action_button(
                        f"cancel_overwrite_{name}",
                        "Cancelar"
                    ),
                    #style="display: flex; justify-content: flex-end;"
                )
            )
        )
    )


def create_modal_warning_exist_model_with_id(name, nombre_version, id_boton):
    return ui.modal(
        ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.div(
                        # Estilo para el texto de advertencia
                        ui.tags.p(
                            f"El modelo en la etapa '{name}' ya existe en la versión '{nombre_version}'. "
                            "Si usted quiere continuar, se le recomienda generar una nueva versión.",
                            style="color: #d9534f; font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 20px;"
                        ),
                        style="padding: 10px; border: 1px solid #d9534f; border-radius: 5px; background-color: #f2dede;"
                    )
                )
            )
        ),
        title=ui.tags.div(
            "⚠️ Advertencia",
            style="color: #f0ad4e; font-size: 20px; font-weight: bold; text-align: center;"
        ),
        easy_close=True,
        size='xs',
        footer=ui.row(
            # Primera fila de botones
            ui.column(
                5,
                ui.tags.div(
                    # Botón "Cancelar"
                    ui.input_action_button(
                        f"{id_boton}",
                        "Cancelar"
                    ),
                    #style="display: flex; justify-content: flex-end;"
                )
            )
        )
    )




def validar_existencia_modelo(modelo_boolean_value , base_datos, version_id=None, json_id=None, dataset_id=None, nombre_modelo=None, nombre_version=None):
    """
    Valida si existe un modelo con un estado de ejecución dado en la base de datos
    y muestra un modal de advertencia si es necesario.

    :param base_datos: Ruta al archivo de la base de datos.
    :param version_id: ID de la versión a validar (opcional).
    :param json_id: ID del JSON a validar (opcional).
    :param nombre_modelo: Nombre del modelo a buscar.
    :param nombre_version: Versión a mostrar en el modal.
    :return: True si el modelo no existe o no tiene estado, False si existe y se muestra el modal.
    """
    # Verificar el estado de ejecución utilizando la función check_execution_status
    if not modelo_boolean_value:  
        #print("valores antes de ejecutar check:" ,modelo_boolean_value , base_datos, version_id, json_id, nombre_modelo,nombre_version)  
        estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id, dataset_id=dataset_id)
        #print(estado_ejecucion, "que estado hay aca? despues de check?")
        if estado_ejecucion is not None and estado_ejecucion == "Exito":
            # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
            ui.modal_show(create_modal_warning_exist_model(nombre_modelo, nombre_version))
            return False  # El modelo ya existe con un estado asociado

        return True  # El modelo no existe o no tiene estado
    

def validar_existencia_modelo_for_files(modelo_boolean_value , base_datos, version_id=None, json_id=None, nombre_modelo=None, nombre_version=None):
    """
    Valida si existe un modelo con un estado de ejecución dado en la base de datos
    y muestra un modal de advertencia si es necesario.

    :param base_datos: Ruta al archivo de la base de datos.
    :param version_id: ID de la versión a validar (opcional).
    :param json_id: ID del JSON a validar (opcional).
    :param nombre_modelo: Nombre del modelo a buscar.
    :param nombre_version: Versión a mostrar en el modal.
    :return: True si el modelo no existe o no tiene estado, False si existe y se muestra el modal.
    """
    # Verificar el estado de ejecución utilizando la función check_execution_status
    if not modelo_boolean_value:
        print()
        estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)
        print(estado_ejecucion, "que estado hay aca?")
        if estado_ejecucion is not None and estado_ejecucion == "Exito":
            # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
            ui.modal_show(create_modal_generic(f"button_files_{nombre_modelo}", f"Tenga en cuenta que ya tiene un modelo generado en {nombre_version}"))
            return True  # El modelo ya existe con un estado asociado

        return False  # El modelo no existe o no tiene estado
    
def validar_existencia_modelo_por_dinamica_de_app(modelo_boolean_value, base_datos, version_id=None, json_id=None, nombre_modelo=None, id_validacion_score=None):
    """
    Valida si existe un modelo con un estado de ejecución dado en la base de datos
    y maneja posibles errores en la consulta.

    :param modelo_boolean_value: Booleano que indica si el modelo debe validarse.
    :param base_datos: Ruta al archivo de la base de datos.
    :param version_id: ID de la versión a validar (opcional).
    :param json_id: ID del JSON a validar (opcional).
    :param id_validacion_score: ID del dataset a validar (opcional).
    :return: True si el modelo ya existe con estado "Éxito", False si no existe o no tiene estado, None si ocurre un error.
    """
    try:
        # Si modelo_boolean_value es False, verificamos la existencia del modelo
        if not modelo_boolean_value:
            print(f"Llamando a check_execution_status con version_id={version_id}, json_id={json_id}, nombre_modelo={nombre_modelo}")
            
            # Llamar a la función que verifica el estado de ejecución
            estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id, dataset_id=id_validacion_score)
            
            if estado_ejecucion is not None and estado_ejecucion == "Exito":
                return True  # El modelo ya existe con estado exitoso

            return False  # El modelo no existe o no tiene estado asociado
        
    except sqlite3.Error as e:
        print(f"Error en la validación del modelo en la base de datos: {e}")
        return None  # Devuelve None en caso de error
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None  # Devuelve None en caso de error inesperado
    
    
def check_if_exist_id_version_id_niveles_scord(version_id, niveles_sc_id):
    """
    Verifica si alguno de los valores es None o está vacío.

    :param version_id: ID de la versión.
    :param niveles_sc_id: ID de los niveles de scoring.
    :return: True si cualquiera de los valores es None o vacío, False en caso contrario.
    """
    return not version_id or not niveles_sc_id



def check_if_exist_id_version(version_id):
    return not version_id



def create_modal_generic(id_button_close, descripcion):
    """
    Crea un modal genérico.

    :param id_button_close: ID del botón de cierre.
    :param descripcion: Descripción o contenido principal del modal.
    :return: Modal Shiny UI.
    """
    # Convertir `descripcion` a string si no lo es
    if not isinstance(descripcion, str):
        descripcion = str(descripcion)

    m = ui.modal(
        ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.div(
                        # Estilo para el texto de advertencia
                        ui.tags.p(
                            descripcion,
                            style="color: #d9534f; font-size: 16px; font-weight: bold; text-align: center; margin-bottom: 20px;"
                        ),
                        style="padding: 10px; border: 1px solid #d9534f; border-radius: 5px; background-color: #f2dede;"
                    )
                )
            )
        ),
        "",
        
        title="⚠️ Advertencia",  # El título debe ser directamente un string
        easy_close=True,
        footer=ui.input_action_link(
            id_button_close,
            "Cerrar",
            class_="btn btn-warning"
        ),
    )
    return m



def tiene_modelo_generado(dataset_id):
    """
    Verifica si un dataset tiene un modelo generado en la tabla 'model_execution'.

    :param dataset_id: El ID del dataset a verificar.
    :return: True si tiene un modelo generado, False en caso contrario.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()

    try:
        # Consulta para verificar si existe un modelo asociado al dataset_id
        query = "SELECT COUNT(*) FROM model_execution WHERE dataset_id = ?"
        cur.execute(query, (dataset_id,))
        count = cur.fetchone()[0]

        # Retorna True si se encontró al menos un modelo, False de lo contrario
        return count > 0
    except sqlite3.Error as e:
        print(f"Error al verificar el modelo generado: {e}")
        return False
    finally:
        conn.close()
        


def obtener_nombre_dataset(version_id=None, json_version_id=None):
    """
    Recupera el nombre del dataset asociado a un modelo en la tabla 'model_execution'.
    Puede filtrar por 'version_id', 'json_version_id' o ambos.

    :param version_id: (Opcional) ID de la versión del modelo.
    :param json_version_id: (Opcional) ID del JSON de la versión.
    :return: Nombre del dataset si se encuentra, de lo contrario, None.
    """
    conn = sqlite3.connect('Modeling_App.db')
    cur = conn.cursor()
    
    try:
        # Construir la consulta de forma dinámica
        query = "SELECT dataset_name FROM model_execution WHERE 1=1"
        params = []

        if version_id is not None:
            query += " AND version_id = ?"
            params.append(version_id)

        if json_version_id is not None:
            query += " AND json_version_id = ?"
            params.append(json_version_id)

        # Ejecutar la consulta
        cur.execute(query, params)
        result = cur.fetchone()
        
        return result[0] if result else None
    
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None
    finally:
        conn.close()