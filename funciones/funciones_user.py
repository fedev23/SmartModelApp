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
    


def show_selected_project_card(user_id, project_id):
    # Buscar el proyecto por ID
    projects = get_user_projects(user_id)
    project = next((proj for proj in projects if str(proj['id']) == project_id), None)
    
    if project:
        sanitized_name =  project['id']
        print(sanitized_name)
        return ui.div(
            f"Proyecto: {project['name']}, Fecha de creación: {project['created_date']}",
            global_user_proyecto.card_desarollo(),
            global_user_proyecto.card_validacion_in_sample(),
            global_user_proyecto.card_out_to_sample_valid(),
            global_user_proyecto.card_produccion(),
            ui.input_action_link(
            f"eliminar_proyect_{sanitized_name}", 
            ui.tags.i(class_="fa fa-trash fa-2x"),  # Ícono de basura
            #class_="btn btn-danger"  # Opcional: estilo de botón rojo
            ),
            id=f"project_card_{sanitized_name}"
        )
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
    
