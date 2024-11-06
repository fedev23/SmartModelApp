from shiny import ui
from funciones.funciones_user import show_selected_project_card
from shiny import App, ui, reactive
from screens.screen3 import screen3
from screens.screen_Resultados import screenResult
from screens.screen_Validacion import screenValid
from screens.screen_desarollo import screenDesarollo
from screens.screen_produccion import screenProduccion
from screens.screen_in_sample import screenInSample
from screens.screen_login import screenLogin
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
from clases.class_resultado import ResultadoClassPrueba
from screens.screen_desarollo import screenDesarollo

screen_User = ui.page_fluid(
    ui.tags.button("SmartModeling", class_="logo-button"),
    #ui.output_ui("create_user_menu"),
    ui.tags.div(
            ui.card(
                ui.output_ui("devolver_acordeon"),
                # sfull_screen=True,
            ),
   
    id="module_container",
    ),
    
    ui.output_ui("create_sidebar"),
    # ui.h3("Tarjeta de Usuario", fillable=True)
    ui.output_ui("despligue_menu"),
    ui.navset_card_tab(
    ui.nav_panel(f"{global_name_desarrollo}", screenDesarollo),
    ui.nav_panel(f"{global_name_in_Sample}", screenInSample),
    ui.nav_panel(f"{global_name_out_of_Sample}", screenValid), #-----> va tener que ser out of sample y scoring
    #ui.nav_panel(f"{global_name_in_Sample}", screenInSample),
    
    ),
)


screenResult = ui.page_fluid(
    ui.div(
        ui.div(
             ui.input_action_button("volver_resultados" ,"SmartModeling", class_="logo-button"), 
        ),
        ui.div(
            ui.output_ui("menu_resultados"),
            ui.h3(ui.output_text("nombre_proyecto_resultados")),
            ui.h3("Resultados",  class_ = "custom-title"),
            ui.navset_card_tab(
                ui.nav_panel(f"{global_name_desarrollo}", 
                        ui.column(4, ui.download_button("descargar_resultados_desarollo", "Descargar Todos los reportes desarollo")),
                        ui.output_ui("render_resultado_card"),
                        ui.output_ui("funcion_volver"),
                        ui.output_ui("render_desarollo_resultado_dos"),
                        ui.output_ui("resultado_card_clean_trans"),
                        #ui.output_ui("html_output_clean"),
                        ui.output_ui("resultado_card_desarollo4"),
                        #ui.output_ui("ver_html_desarollo"),
                        ui.output_ui("html_output_desarollo2"),
                        ui.output_ui("html_output_desarollo3"),
                    
                     value="desarollo"
                ),
                ui.nav_panel(f"{global_name_in_Sample}", 
                        ui.column(4, ui.download_button("descargar_resultados_validacion", "Descargar Todos los reportes validacion")),
                        ui.output_ui("resultado_card_validacion_in_sample"),
                    value= "in_sample"
                ),
                ui.nav_panel(f"{global_name_out_of_Sample}", 
                        ui.column(4, ui.download_button("descargar_resultados_validacion_out_to_sample", "Descargar Todos los reportes validacion")),
                         ui.output_ui("resultado_card_validacion_out_to_sample"),
                         ui.output_ui("dynamic_ui"),
                        ui.output_ui("download_ui"),
                    
                        value= "out_to_sample"
                ),
                ui.nav_panel(f"{global_name_produccion}", 
                        ui.column(4, ui.download_button("descargar_resultados_produccion", "Descargar Todos los reportes validacion")),
                        ui.output_ui("resultado_card_produccion"),
                    value="produccion"
                ),
                 id="Resultados_nav"
            ),
        ),
        
    ),
)
