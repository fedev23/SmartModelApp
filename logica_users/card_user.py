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

        # Inicializar `project_options` con un valor por defecto
        project_options = {}

        if projects:
            project_options = {
                str(project['id']): project['name'] for project in projects
            }

        return ui.page_fluid(
            # Contenedor principal con clase de Bootstrap para centrar el contenido
            ui.div(
                ui.div(
                    # Tarjeta con el contenido
                    ui.div(
                        # Sección de carga de archivos
                        ui.input_file("file_desarollo", "Upload File"),
                        ui.br(),
                        
                        ui.div(
                         ui.input_action_button(f"start_{name_suffix}", "+ Create Project", class_="btn btn-dark me-2"),
                         class_="d-flex justify-content-start mb-3"
                        ),

                        # Botones de creación
                        ui.div(
                            ui.input_action_button(f"version_{name_suffix}", "+ Create Version", class_="btn btn-dark me-2"),
                            #ui.input_action_button(f"dataset_{name_suffix}", "+ Create Dataset", class_="btn btn-dark"),
                            class_="d-flex justify-content-start mb-3"  # Centrar los botones de creación
                        ),

                        # Menús desplegables con elementos adicionales
                        ui.div(
                            # Añadir los selectores en una fila con espacio entre ellos
        
                            ui.input_select("other_select", "Select Version", {"a": 'a'}, #class_="me-3"
                                            ),
                            ui.input_select("files_select", "Select Dataset", {"a": 'a'}),
                            class_="d-flex justify-content-start"  # Alinear los selectores a la izquierda
                        ),
                        class_="card-body"
                    ),
                    class_="card"
                )
            )
        )
