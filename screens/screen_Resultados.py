
from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion


from clases.class_resultado import ResultadoClassPrueba

screenResult = ui.page_fluid(
    ui.div(
        ui.div(
             ui.input_action_button("volver_resultados" ,"SmartModel", class_="logo-button"), 
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
                        ui.column(4, ui.download_button("descargar_resultados_validacion", "Descargar Todos los reportes validación in sample")),
                        ui.output_ui("resultado_card_validacion_in_sample"),
                    value= "in_sample"
                ),
                ui.nav_panel(f"{global_name_out_of_Sample}", 
                        ui.column(4, ui.download_button("descargar_resultados_validacion_out_of_sample", "Descargar Todos los reportes Out-of-Sample")),
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
