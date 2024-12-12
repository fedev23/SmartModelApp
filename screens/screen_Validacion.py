from shiny import App, ui, reactive
from global_names import global_name_out_of_Sample
from clases.global_sessionV2 import *


#projects = global_session_V2.get_opciones_name_dataset_Validation_sc()
screenValid = ui.page_fluid(
        ui.div(
        ui.row(
            ui.column(
                12, 
                ui.div(
                    ui.div(class_="mt-5"),
                    ui.div(
                    ui.input_select(
                        "files_select_validation_scoring",
                        "",
                        [],
                        width="100%"
                    ),
                    style="padding: 20px; height: 100px;"  # Ajusta el padding y la altura en el contenedor
                ),
                    #ui.HTML("<div style='width: 15px;'></div>"),
                    ui.div(
            ui.input_file(
                "file_validation",
                "",
                placeholder="Seleccione un archivo",
                button_label="+",
                accept=[".csv", ".txt"],
                width="100%"
            ),
            style="padding: 12px; height: 60px;"  # Ajusta el padding y la altura en el contenedor
        ),
                    ui.div(
                        ui.output_ui("remove_dataset_data_alidacionSC"),
                        style="padding: 12px; height: 60px;"  
                    ),
                    ui.HTML("<div style='width: 10px;'></div>"),
                    class_="d-flex justify-content-end:",
                    style="gap: 10px; margin-top: -5px;"
                )
            )
        ), 
         ui.div(class_="mt-2"),
        # Tarjeta para mostrar datos de validación
        ui.card(
            # Encabezado de la tarjeta
            ui.card_header("Datos de" " " f"{global_name_out_of_Sample}"),
            # Salida del DataFrame de resumen
            ui.output_data_frame("summary_data_validacion_out_to_sample"),
            ui.output_text("error_in_validacion"),  # Salida UI adicional
        ),
    ),

    ui.input_radio_buttons(  
        "radio_models",  
        "Validacion",
        {"1": "Full", "2": "Scoring"},  
         inline=True,
         selected=1,
    ),
    
    #ui.input_text_area(placeholder="Ingrese el ")
    
    ui.output_ui("seleccionador_target"),

    ui.tags.hr(),
    ui.div(class_="mt-5"),
    ui.navset_card_underline(
        ui.nav_panel(
            "Ejecución",
            ui.output_text_verbatim("mostrar_out_of_sample"),
            ui.output_ui("card_out_to_sample"),
            ui.output_ui("card_produccion1"),
            
            ui.output_ui("open_of_sample"),
            ui.output_ui("mostrar_fin_Sample"),
            ui.output_ui("mostrarDescarga_out"),
            ui.output_ui("busy_indicator_of_sample"),
            value="out_to_sample"
        ),
        ui.nav_spacer(),
        ui.nav_panel(
            "Resultados Scoring & validation",
            ui.div(
                ui.card(
                    ui.column(4, ui.download_button("descargar_resultados_validacion_out_to_sample",
                                                    "Descargar Todos los reportes validacion")),
                    ui.output_ui(
                        "resultado_card_validacion_out_to_sample"),
                    ui.output_ui("dynamic_ui"),
                    ui.output_ui("download_ui"),

                    ui.column(4, ui.download_button(
                        "descargar_resultados_produccion", "Descargar Todos los reportes Scoring")),
                    ui.output_ui("resultado_card_produccion"),
                    value="produccion"

                )
            )

        ),

    ),
    ui.div(class_="mt-5"),




),
