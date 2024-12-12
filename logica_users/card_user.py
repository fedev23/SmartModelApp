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

            return ui.page_fluid(
                # Fila principal con seleccionadores y botones alineados
                ui.row(
                    # Seleccionador 1 y botón Crear Proyecto
                    ui.column(
                        6,
                        ui.row(
                            ui.div(
                                 ui.input_select(
                                "project_select",
                                "",
                                project_options,
                                width="50%"
                            ),
                                #ui.column(1, ui.HTML("<div style='width: 20px;'></div>")),
                                #class_="d-flex justify-content-center",  
                                ),
                           
                        ),
                    ),
                     ui.column(
                            6,
                            ui.div(
                                ui.input_action_button(
                                f"start_{name_suffix}",
                                "+ Crear Proyecto",
                                style="font-size: 15px; padding: 8px 10px;",
                                class_="btn btn-dark btn-sm me-2",
                            ),
                            ui.output_ui("project_card_container"),
                            #class_="d-flex align-items-center gap-1 mb-1",
                            #style="margin-top: -3px;"   
                            )
                        )
                    
                ),
                    # Seleccionador 2 y botón Crear Versión
                    ui.row(
                         ui.column(
                        6,
                        #ui.row(
                        ui.div(
                            ui.input_select(
                                "other_select",
                                "",
                                {"a": "a"},
                                width="50%"
                            ),
                        )
                    ),
                    ui.column(
                        6,
                        ui.div(
                         ui.input_action_button(
                                f"version_{name_suffix}",
                                "+ Crear Versión",
                               style="font-size: 15px; padding: 8px 10px;",
                                class_="btn btn-dark btn-sm me-2",
                            ),
                            ui.output_ui("button_remove_versions"), 
                            #style="font-size: 15px; padding: 8px 10px;",
                            #class_="btn btn-dark btn-sm me-2",   
                        )
                        
                        ),
                        
                    ),
                            
                       
                    # Seleccionador de Archivos y InputFile alineados correctamente
                    ui.column(
                        12,
                        ui.div(
                            ui.input_select(
                                "files_select",
                                "",
                                {'a': "Archivo A", 'b': "Archivo B"},
                                width="50%",
                                #style="margin-top: -2px;"
                            ),  ui.HTML("<div style='width: 15px;'></div>"),
                            
                            ui.div(
                                ui.input_file(
                                    "file_desarollo",
                                    "",
                                    placeholder="Seleccione un archivo",
                                    button_label="+",
                                    accept=[".csv", ".txt"],
                                    width="100%"
                                ),

                            ),
                            ui.HTML("<div style='width: 10px;'></div>"),
                            ui.output_ui("remove_dataset"),  
                            class_= "d-flex justify-content-end:" , 
                            style="margin-top: -5px;"          
                            #class_="file-input-container d-flex align-items-center gap-3 mb-3"
                        ),
                        
                    )
                ),
            