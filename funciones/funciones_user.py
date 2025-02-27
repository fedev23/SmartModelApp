from api.db import *
from shiny import ui, reactive
import re
from clases.class_user_proyectName import global_user_proyecto

proyectos_usuario = reactive.Value([])


def actualizar_ui():
    @reactive.Value
    def actualizar_lista_proyectos(user_id):
        """Función que actualiza la lista reactiva de proyectos para el usuario actual."""
        proyectos_usuario.set(get_user_projects(
            user_id))  # Actualiza con los proyectos actuales del usuario


def create_project_selector(user_id):
    # Obtener proyectos del usuario
    projects = get_user_projects(user_id)

    if projects:
        # Crear opciones para el selector
        project_options = {str(project['id']): project['name']
                           for project in projects}

        # Crear el selector de proyecto y contenedor para la tarjeta del proyecto
        return ui.div(
            ui.input_select(
                "project_select",
                "Selecciona un proyecto:",
                project_options
            ),

            # Este contenedor mostrará la tarjeta del proyecto seleccionado
            ui.output_ui("project_card_container")
        )
    else:
        return ui.div("No hay proyectos disponibles para este usuario.")


def create_project_ui(projects):
    if projects:
        # Construye las opciones del selector a partir de los proyectos
        project_options = {str(project['id']): project['name']
                           for project in projects}
        # versions_options = {str(versions['id']): versions['name'] for version in versions}
        # print(versions_options)
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
                        {"a": 'a'},
                        width="60%"
                    )
                )
            ),
            # Contenedor para la tarjeta del proyecto
            ui.output_ui("project_card_container"),
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


def create_version_ui(projects):
    if projects:
        # Construye las opciones del selector a partir de los proyectos
        project_options = {str(project['id']): project['name']
                           for project in projects}
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
                    ),
                    ui.output_ui("project_card_container")
                )
            )
        )


def show_selected_project_card(user_id, project_id):
    # Obtener los proyectos del usuario
    projects = get_user_projects(user_id)
    try:
        # Convertir el project_id a entero
        project_id_int = int(project_id)
    except ValueError:
        return ui.div("")

    # Buscar el proyecto con el ID correspondiente
    project = next(
        (proj for proj in projects if proj['id'] == project_id_int), None)

    if project:
        sanitized_name = project['id']
        return ui.input_action_link(
            f"eliminar_proyect_{sanitized_name}",
            ui.tags.i(
                class_="fa fa-trash fa-2x",
                style="""
        color: #C82333;  /* Rojo más discreto */
        background: none; 
        border: none;
        transition: color 0.2s ease-in-out, transform 0.1s ease-in-out;
        cursor: pointer;
    """,
                onmouseover="this.style.color='#A52A2A'; this.style.transform='scale(1.05)';",
                onmouseout="this.style.color='#C82333'; this.style.transform='scale(1)';"
            )

        )
    else:
        print("No se encontró el proyecto.")
        return ui.div("No hay proyectos.")


def button_remove_version(project_id, target_version_id):
    # Obtiene la lista de versiones asociadas al proyecto
    versions_list = get_project_versions(project_id)

    # Si no hay versiones asociadas, no intentes buscar una versión específica
    if not versions_list:
        return None  # No hay botón de eliminación porque no hay versiones

    # Busca si la versión especificada pertenece al proyecto
    version = next((version for version in versions_list if str(
        version['version_id']) == str(target_version_id)), None)

    if version:
        sanitized_name = version['version_id']  # Obtén el ID de la versión
        # Devuelve un enlace de acción para eliminar la versión
        return ui.input_action_link(
            f"eliminar_version_{sanitized_name}",
            ui.tags.i(
                class_="fa fa-trash fa-2x",
                style="""
        color: #C82333;  /* Rojo más discreto */
        background: none; 
        border: none;
        transition: color 0.2s ease-in-out, transform 0.1s ease-in-out;
        cursor: pointer;
    """,
                onmouseover="this.style.color='#A52A2A'; this.style.transform='scale(1.05)';",
                onmouseout="this.style.color='#C82333'; this.style.transform='scale(1)';"
            )
        )

    else:
        return None


def button_remove(versions_list, target_version_id, id, name):

    # Busca si la versión especificada pertenece al proyecto
    version = next((version for version in versions_list if str(
        version.get(id)) == str(target_version_id)), None)

    if version:
        sanitized_name = version[id]  # Obtén el ID de la versión
        # Devuelve un enlace de acción para eliminar la versión
        return ui.input_action_link(
            f"eliminar_version_{sanitized_name}_{name}",
            ui.tags.i(
                class_="fa fa-trash fa-2x",
                style="""
        color: #C82333;  /* Rojo más discreto */
        background: none; 
        border: none;
        transition: color 0.2s ease-in-out, transform 0.1s ease-in-out;
        cursor: pointer;
    """,
                onmouseover="this.style.color='#A52A2A'; this.style.transform='scale(1.05)';",
                onmouseout="this.style.color='#C82333'; this.style.transform='scale(1)';"
            )
        )
    else:
        print(
            f"No se encontró una versión con {id} igual a {target_version_id} en la lista.")
        return None


def create_modal_eliminar_bd(name_proyecto):
    m = ui.modal(ui.input_action_button("eliminar_proyecto","Eliminar Proyecto", class_="btn btn-danger"),
        ui.input_action_button("cancelar_eliminar", "Cancel", class_="custom-cancel-button"),
        title=f"¿Estás seguro de que quieres eliminar el proyecto '{name_proyecto}'?",
        easy_close=True,
        footer=None,
    )
    ui.modal_show(m)


def create_modal_v2(titulo, boton_confirmar_label, boton_cancelar_label, id_boton_confirmar, id_boton_cancelar):
    m = ui.modal(
        ui.input_action_button(
            id_boton_confirmar, boton_confirmar_label, class_="btn btn-danger"),
        ui.input_action_button(
            id_boton_cancelar, boton_cancelar_label, class_="custom-cancel-button"),
        title=titulo,
        easy_close=True,
        footer=None,
    )
    ui.modal_show(m)


def create_modal_versiones(id_proyecto):
    m = ui.modal(
        ui.row(
            ui.column(12, ui.input_text(f"name_version",
                      f"tipo de version del proyecto {id_proyecto}", width="100%")),
        ),
        ui.div(
            ui.div(
                ui.input_action_button(
                    "continuar_version", "Continuar", class_="custom-ok-button", style="text-align: left"),
                ui.input_action_button(
                    "cancelar_version", "Cancelar", class_="custom-cancel-button"),
            ),
        ),
        title="Nueva versión",
        easy_close=True,
        footer=None,
        size='m',
        fade=True,
    )
    ui.modal_show(m)


def create_modal_versiones_param(id_proyecto, id_version):
    m = ui.modal(
        ui.row(
            ui.column(12, ui.input_text(f"name_version_param",
                      f" Version de parametros para el  {id_proyecto} en la version {id_version}", width="100%")),
        ),
        ui.div(
            ui.div(
                ui.input_action_button(
                    "continuar_version_param", "Continuar", class_="custom-ok-button", style="text-align: left"),
                ui.input_action_button(
                    "cancelar_version_param", "Cancelar", class_="custom-cancel-button"),
            ),
        ),
        title="Nueva versión de parametros",
        easy_close=True,
        footer=None,
        size='m',
        fade=True,
    )
    ui.modal_show(m)
