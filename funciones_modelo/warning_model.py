from shiny import ui
from api.db.sqlite_utils import *
from funciones_modelo.help_models import *
def create_modal_warning_exist_model(name, nombre_version):
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




def validar_existencia_modelo(modelo_boolean_value , base_datos, version_id=None, json_id=None, nombre_modelo=None, nombre_version=None):
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
        
        estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)
        print(estado_ejecucion, "que estado hay aca?")
        if estado_ejecucion is not None and estado_ejecucion == "Exito":
            # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
            ui.modal_show(create_modal_warning_exist_model(nombre_modelo, nombre_version))
            return False  # El modelo ya existe con un estado asociado

        return True  # El modelo no existe o no tiene estado
    

def validar_existencia_modelo_for_models(modelo_boolean_value , base_datos, version_id=None, json_id=None, nombre_modelo=None, nombre_version=None):
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
        
        estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)
        print(estado_ejecucion, "que estado hay aca?")
        if estado_ejecucion is not None and estado_ejecucion == "Exito":
            # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
            ui.modal_show(create_modal_warning_exist_model(nombre_modelo, nombre_version))
            return False  # El modelo ya existe con un estado asociado

        return True  # El modelo no existe o no tiene estado
    

def validar_existencia_modelo_por_dinamica_de_app(modelo_boolean_value , base_datos, version_id=None, json_id=None):
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
        print(f"Llamando a check_execution_status con version_id={version_id}, json_id={json_id}")
        estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)
        if estado_ejecucion is not None and estado_ejecucion == "Exito":
            return True  # El modelo ya existe con un estado asociado

        return False  # El modelo no existe o no tiene estado
    
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
