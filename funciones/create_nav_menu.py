from shiny import ui
from clases.class_user_proyectName import global_user_proyecto
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion

def create_nav_menu(name_suffix, name):
    return ui.page_fluid(ui.navset_bar(
        ui.nav_control(ui.input_action_link(f"start_{name_suffix}", f"Comenzar proyecto")),       
    )
    )