from shiny import ui
from clases.reactives_name import global_names_reactivos
from clases.global_session import global_session
from global_names import mensaje_por_defecto
from clases.global_reactives import global_estados
from clases.global_sessionV3 import *

def create_nav_menu_user(name_suffix):

    return ui.page_navbar(
        ui.nav_control(ui.p(
            f"Proyecto: {global_session_V3.name_proyecto_original.get() or 'No hay un proyecto'}", class_="styled-text")),
        ui.nav_control(ui.p(
            f"Versión: {global_session_V3.name_version_original.get() or 'Versión por defecto'}", class_="styled-text")),
        ui.nav_control(ui.p(
            f"Archivo: {global_names_reactivos.get_name_file_db() or 'No hay un DataSet seleccionado'}", class_="styled-text")),
        ui.nav_control(ui.p(
            f"Version Niveles & Scorcards: {global_session_V3.name_version_niveles_score_original.get() or 'Versión por defecto'}", class_="styled-text")),
        ui.nav_spacer(),
        
        ui.nav_control(ui.input_dark_mode(id="dark_mode_switch",mode="light",class_="dark-mode-toggle")),
        
        id=f"tab_{name_suffix}",
        title="",
        selected=None,
        inverse=False,
        position='sticky-top',  # Esto hace que se mueva con el contenido
        # bg="night",
        bg="transparent",
        # class_="styled-nav",  # Aplicar la clase personalizada



    )
