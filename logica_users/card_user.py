from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import *
from clases.global_session import global_session
from clases.global_reactives import global_estados


def user_ui(input: Inputs, output: Outputs, session: Session, name_suffix):

   
    @output
    @render.ui  
    def devolver_acordeon():
        projects = global_session.get_proyectos_usuarios()  # Obtiene la lista actual de proyectos

        if projects:
            project_options = {
                str(project['id']): project['name'] for project in projects
            }

            return ui.div(
                ui.row(
                    # Primera columna para el botón y el selector de proyectos
                    ui.column(
                        6,  # Ancho de la columna
                        # Botón para crear proyecto, alineado con el selector
                        ui.input_action_button(
                            f"start_{name_suffix}", 
                            "+ Crear Proyecto", 
                            class_="btn btn-dark mb-2"
                        ),
                        ui.input_select(
                            "project_select",
                            "",
                            project_options,
                            width="100%"  # Asegura que el selector ocupe todo el ancho disponible
                        ),
                        ui.output_ui("project_card_container"),  # Alineado debajo del selector
                    ),
                    # Segunda columna para el botón y el selector de versiones
                    ui.column(
                        6,  # Ancho de la columna
                        # Botón para crear versión, alineado con el selector
                        ui.input_action_button(
                            f"version_{name_suffix}", 
                            "+ Crear Versión", 
                            class_="btn btn-dark mb-2"
                        ),
                        ui.input_select(
                            "other_select",
                            "",
                            {"a": "a"},
                            width="100%"  # Asegura que el selector ocupe todo el ancho disponible
                        ),
                        ui.output_ui("button_remove_versions"),  # Alineado debajo del selector
                    ),
                ),
                ui.div(class_="mt-5"),  # Espaciado entre las filas

                # Fila para el input de archivo y el selector de datasets debajo de la carga de archivo
                ui.row(
                    ui.column(
                        12,  # Ancho de la columna para el input de archivo
                        # Input de carga de archivo
                        ui.input_file(
                            "file_desarollo",
                            "" ,
                            placeholder="Seleccione un archivo",
                            button_label=ui.tags.i(class_="fa fa-upload fa-sm"),
                            accept=[".csv", ".txt"],
                            width="40%",  # Asegura que el input ocupe todo el ancho de la columna
                            
                        ),
                        
                    )
                ),

                # Fila para el selector de datasets, ahora independiente de la tarjeta
                ui.row(
                    ui.column(
                        12,  # Ancho de la columna para el selector de datasets
                        ui.input_select(
                            "files_select",
                            "",
                            {'a': "a"},
                            width="40%"  # Asegura que el selector ocupe todo el ancho de la columna
                        ),
                        ui.output_ui("remove_dataset"),  # Alineado debajo del selector
                    )
                )
            )
