from shiny import ui
from api.db.sqlite_utils import *
from funciones_modelo.help_models import *

def create_modal_warning_exist_model(name, nombre_version):
    return ui.modal(
        ui.tags.div(
            ui.row(
                ui.column(
                    12,
                    ui.tags.p(
                        f"El modelo en la etapa '{name}' ya existe en la versión {nombre_version}."
                        "Si usted quiere continuar, se le recomienda generar una nueva versión ."
                    )
                ),
            )
        ),
        title="Advertencia",
        easy_close=True,
        size='xs',
        footer=ui.tags.div(
            #ui.input_action_button(f"continue_overwrite_{name}", "Continuar", style="margin-right: 10px;"),
            ui.input_action_button(f"cancel_overwrite_{name}", "Cancelar"),
            style="display: flex; justify-content: flex-end;"
        )
    )



def validar_existencia_modelo(base_datos, version_id=None, json_id=None, nombre_modelo=None, nombre_version=None):
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
    estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)

    if estado_ejecucion is not None:
        # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
        ui.modal_show(create_modal_warning_exist_model(nombre_modelo, nombre_version))
        print(f"Modelo '{nombre_modelo}' con versión '{nombre_version}' ya existe con estado: {estado_ejecucion}.")
        return False  # El modelo ya existe con un estado asociado

    print(f"Modelo '{nombre_modelo}' con versión '{nombre_version}' no existe o no tiene estado asociado.")
    return True  # El modelo no existe o no tiene estado