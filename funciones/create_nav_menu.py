from shiny import ui
from clases.class_user_proyectName import global_user_proyecto
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion

def create_nav_menu(name_suffix, name):
    return ui.page_fluid(ui.navset_bar(
        ui.nav_control(ui.input_action_link(f"start_{name_suffix}", f"Comenzar proyecto")),       
    
            ui.nav_menu(
                f"Panel de carga",
                ui.nav_control(
                    ui.input_action_link(f"screen_Desarollo_{name_suffix}", f"{global_name_desarrollo}"),
                    ui.input_action_link(f"screen_in_sample_{name_suffix}", f"{global_name_in_Sample}"),
                    ui.input_action_link(f"load_Validacion_{name_suffix}", f"{global_name_out_of_Sample}"),
                    ui.input_action_link(f"screen_Produccion_{name_suffix}", f"{global_name_produccion}")
                ),
            ),
            ui.nav_control(ui.input_action_link(f"load_param_{name_suffix}", f"Ejecutar {name}")), 
            ui.nav_control(ui.input_action_link(f"ir_result_{name_suffix}", f"Panel de resultados")),
            ui.nav_menu(
                f"Más opciones ",
                ui.nav_control(
                    #ui.input_dark_mode(mode="light"),
                    ui.input_action_link(f"settings_{name_suffix}", f"Cerrar sesión"),
                ),
            ),
            id=f"tab_{name_suffix}",
            title="",
            selected=None,
            inverse=False,
                bg="night",   
        ),
                            
        ui.h3(ui.output_text(f"nombre_proyecto_{name_suffix}")),
        
    )
   
   