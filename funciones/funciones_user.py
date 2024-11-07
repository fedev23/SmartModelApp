from api.db import *
from shiny import ui, reactive
import re
from clases.class_user_proyectName import global_user_proyecto

proyectos_usuario = reactive.Value([])

def actualizar_ui():
    @reactive.Value
    def actualizar_lista_proyectos(user_id):
        """Función que actualiza la lista reactiva de proyectos para el usuario actual."""
        proyectos_usuario.set(get_user_projects(user_id))  # Actualiza con los proyectos actuales del usuario



def create_project_selector(user_id):
    # Obtener proyectos del usuario
    projects = get_user_projects(user_id)
    
    if projects:
        # Crear opciones para el selector
        project_options = {str(project['id']): project['name'] for project in projects}
        
        # Crear el selector de proyecto y contenedor para la tarjeta del proyecto
        return ui.div(
            ui.input_select(
                "project_select",
                "Selecciona un proyecto:",
                project_options
            ),
            
            ui.output_ui("project_card_container")  # Este contenedor mostrará la tarjeta del proyecto seleccionado
        )
    else:
        return ui.div("No hay proyectos disponibles para este usuario.")
    
    


def create_project_ui(projects):
    if projects:
        # Construye las opciones del selector a partir de los proyectos
        project_options = {str(project['id']): project['name'] for project in projects}

        # Devuelve la estructura de la UI
        return ui.div(
            ui.row(
                ui.column(
                    6,  # Ajusta el ancho según sea necesario
                    ui.input_select(
                        "project_select",
                        "Selecciona un proyecto:",
                        project_options,
                        width="60%"
                    )
                ),
                ui.column(
                    6,  # Otro ancho para el segundo selector
                    ui.input_select(
                        "other_select",
                        "Versiones",
                        {
                            "opcion1": "Opción 1",
                            "opcion2": "Opción 2",
                            "opcion3": "Opción 3"
                        },
                        width="60%"
                    )
                )
            ),
            ui.output_ui("project_card_container"),  # Contenedor para la tarjeta del proyecto
            ui.div(class_="mt-2"),
            ui.div(
                ui.input_file(
                    "file_desarollo",  # ID del input de archivo
                    "Cargar archivo de datos:",
                    button_label='Seleccionar archivo',
                    placeholder='Selecciona un archivo',
                    accept=[".csv", ".txt"],
                    width="30%"
                ),
                # Agrega margen superior para separación
            )
        )
    else:
        # Si no hay proyectos, devuelve un mensaje
        return ui.div("No hay proyectos disponibles.")

    


def show_selected_project_card(user_id, project_id):
    # Buscar el proyecto por ID
    projects = get_user_projects(user_id)
    project = next((proj for proj in projects if str(proj['id']) == project_id), None)
    
    if project:
        sanitized_name =  project['id']
        return  ui.input_action_link(
            f"eliminar_proyect_{sanitized_name}", 
            ui.tags.i(class_="fa fa-trash fa-2x"),  # Ícono de basura
            #class_="btn btn-danger"  # Opcional: estilo de botón rojo
            ),
    else:
        return ui.div("No hay proyectos.")
    
    

    
    


def create_modal_eliminar_bd():
    m = ui.modal(  
            ui.input_action_button("eliminar_proyecto_modal", "Eliminar Proyecto", class_="btn btn-danger"),
            ui.input_action_button("cancelar_eliminar", "Cancel", class_="custom-cancel-button"),
            title="¿Estás seguro de que quieres eliminar este proyecto?",  
            easy_close=True,  
            footer=None,  
        )  
    ui.modal_show(m)
    
