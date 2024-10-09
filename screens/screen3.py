from shiny import ui

screen3 = ui.page_fluid(
        ui.div(
            ui.input_action_button("volver_modelo" ,"SmartModel", class_="logo-button"), 
        ),
        ui.output_ui("menu_modelo"),
         ui.h3(ui.output_text("nombre_proyecto_modelo")),
        ui.h4("Ejecución", class_ = "custom-title" ),
        ui.accordion(
            ui.accordion_panel(
                "Desarrollo" ,
                ui.output_ui("card_desarollo2"),
                ui.output_ui("tarjeta_desarollo"),
                ui.output_ui("mensaje_desarollo"),
                ui.output_text_verbatim("mostrarDatos"),
                #ui.output_text_verbatim("mensaje_id"),
                ui.output_ui("boton_desarollo"),
                ui.output_ui("descarga_desarollo"),
                value="desarrollo"
            ),
            ui.accordion_panel(
                "Validación In sample",
                ui.output_ui("mostrar_fin_inSample"),
                ui.output_ui("card_in_sample"),
                ui.output_ui("open_in_sample"),
                #ui.output_ui("descarga_in_sample"),
                ui.output_ui("busy_indicator_in_sample"),
                ui.output_text_verbatim("mostrar_in_sample"),
                value="in_sample"
            ),
            
             ui.accordion_panel(
                "Validación Out of sample",
                ui.output_text_verbatim("mostrar_out_of_sample"),
                ui.output_ui("card_out_to_sample"),
                ui.output_ui("open_of_sample"),
                ui.output_ui("mostrar_fin_Sample"),
                ui.output_ui("mostrarDescarga_out"),
                ui.output_ui("busy_indicator_of_sample"),
                value="out_to_sample"
            ),
            ui.accordion_panel(
                "Producción",
                ui.output_text_verbatim("mostrar_produccion"),
                ui.output_ui("card_produccion1"),
                ui.output_ui("open_produccion"),
                ui.output_ui("mostrar_mensja_produccion"),
                #ui.output_ui("descarga_produccion"),
                ui.output_ui("busy_indicator_produccion"),
                value="Produccion"
            ),
            id="my_accordion",  # ID para controlar el estado del acordeón desde el servidor
        
        ),
    )
