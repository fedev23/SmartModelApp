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
                        ui.h4("Data Management", class_="card-header text-center"),  # Título centrado
                        
                        ui.div(
                            # Sección de carga de archivos
                            ui.input_file("file_desarollo", "Upload File"),
                            ui.br(),

                            # Botones de creación
                            ui.div(
                                ui.input_action_button(f"start_{name_suffix}", "+ Create Project", class_="btn btn-dark me-2"),
                                ui.input_action_button(f"version_{name_suffix}", "+ Create Version", class_="btn btn-dark"),
                                class_="d-flex justify-content-center mb-3"  # Centrar los botones
                            ),

                            # Menús desplegables con elementos adicionales
                            ui.div(
                                # Añadir las UI outputs a la izquierda de los selectores
                                ui.output_ui("project_card_container"),
                                ui.input_select("project_select", "Select Project", project_options),
                               

                                ui.input_select("other_select", "Select Version", {"a": 'a'}),
                                #ui.output_ui("button_remove_versions"),
                            
                                ui.input_select("files_select", "Select Dataset", {"a": 'a'}),
                                #ui.output_ui("remove_dataset"),
                                class_="d-flex justify-content-center"  # Centrar los menús desplegables
                            ),
                            class_="card-body"
                        ),
                        class_="card"
                    ),
                    #class_="container mt-5 mb-5"  # Márgenes superior e inferior para centrar
                ),
                #class_="d-flex justify-content-center align-items-center vh-100"  # Centrado vertical y horizontal
            )
        )
