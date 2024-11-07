from shiny import App, ui, reactive
from global_names import global_name_out_of_Sample

# Opciones para los tipos de delimitador disponibles
CHOICES = {
    "tipo": [",", '\\t', "' '", ";", "|"],
}

# Definición de la pantalla de validación
screenValid = ui.page_fluid(
    ui.div(
        # ui.h3(f"{global_name_out_of_Sample}", class_="custom-title"),  # Título principal
        ui.h4("Dataset"),  # Subtítulo
        ui.column(12,
                  ui.input_file("file_validation", "Seleccion de archivo CSV o TXT",
                                button_label='Cargar archivo',
                                placeholder='Buscar el archivo',
                                accept=[".csv", ".txt"],
                                width="100%")  # Input para carga de archivos CSV o TXT
                  ),
        # Tarjeta para mostrar datos de validación
        ui.card(
            # Encabezado de la tarjeta
            ui.card_header("Datos de" " " f"{global_name_out_of_Sample}"),
            # Salida del DataFrame de resumen
            ui.output_data_frame("summary_data_validacion_out_to_sample"),
            ui.output_text("error_in_validacion"),  # Salida UI adicional
        ),
    ),


    ui.tags.hr(),
    ui.div(class_="mt-5"),
    ui.navset_card_underline(
        ui.nav_panel(
            "Ejecución",
            ui.output_text_verbatim("mostrar_out_of_sample"),
            ui.output_ui("card_out_to_sample"),
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
                    
                    ui.column(4, ui.download_button("descargar_resultados_produccion", "Descargar Todos los reportes validacion")),
                        ui.output_ui("resultado_card_produccion"),
                    value="produccion"

                )
            )

        ),
        
    ),
    ui.div(class_="mt-5"),
    



),
