from shiny import ui
from api.db.sqlite_utils import *

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



def validar_existencia_modelo(base_datos, version_id, nombre_modal, nombre_version):
    """
    Valida si existe un modelo dado en la base de datos y muestra un modal de advertencia si es necesario.

    :param base_datos: Ruta al archivo de la base de datos.
    :param version_id: ID de la versión a validar.
    :param nombre_modelo: Nombre del modelo a buscar.
    :param nombre_modal: Nombre a mostrar en el modal.
    :param nombre_version: Versión a mostrar en el modal.
    :return: True si el modelo no existe, False si existe y se muestra el modal.
    """
    ult_model = obtener_ultimo_modelo_por_version_y_nombre(base_datos, version_id, nombre_modal)
    if ult_model and ult_model["model_name"] is not None:
        # Mostrar el modal de advertencia si el modelo existe
        ui.modal_show(create_modal_warning_exist_model(nombre_modal, nombre_version))
        return False  # El modelo existe
    return True  # El modelo no existe
