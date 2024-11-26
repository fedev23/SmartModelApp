from shiny import App, ui, reactive
from clases.global_sessionV2 import global_session_V2
from clases.global_session import *

# NECESITO CREAR UNA LISTA REACTIVA PARA QUE SE ACTUALICE CORRECTAMENRE CRREO


def crate_file_input_y_seleccionador():
    # Obtiene la lista actual de proyectos
    projects = global_session_V2.get_opciones_name_dataset_Validation_sc()

    if projects:
        return ui.div(
            ui.column(
                12, ui.div(
                    ui.input_file(
                        "file_validation",
                        "",
                        placeholder="Seleccione un archivo",
                        button_label="+",
                        accept=[".csv", ".txt"],
                        width="50%"
                    ),

                ),
                ui.div(
                    ui.input_select(
                        "files_select_validation_scoring",
                        "",
                        projects,
                        width="50%"
                    ),
                    # ui.output_ui("remove_dataset"),
                    ui.output_ui("remove_dataset_data_alidacionSC"),
                    class_="file-input-container d-flex align-items-center gap-3 mb-3"
                ),

            ),
        )
