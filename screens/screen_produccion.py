from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.create_param import create_screen

CHOICES = {
    "tipo": [",", '\\t', "' '", ";", "|"],
}

screenProduccion = ui.page_fluid(
        ui.div(
            ui.input_action_button("volver_produccion", "SmartModeling", class_="logo-button"),
        ),
        ui.output_ui("nav_out_to_produccion"),
        ui.div(
            ui.h3("Producción", class_="custom-title"),
            ui.h4("Dataset"),  
            ui.column(12, 
            ui.input_file("file_produccion", "Seleccion de archivo CSV o TXT", 
                button_label='Cargar archivo', 
                placeholder='Buscar el archivo', 
                accept=[".csv", ".txt"], 
                width="100%")  # Input para carga de archivos CSV o TXT
        )
        ),
            ui.row(
                ui.column(12, ui.output_text_verbatim("file_status_produccion")),
                #ui.output_ui("update_action_button"),
            ),
            ui.div(
                ui.card(
                    ui.card_header("Datos de Produccion"),
                    ui.output_data_frame("summary_data_produccion"),
                    ui.output_ui("mostrarOut_produccion"),
                    ui.output_text("error_in_produccion")
                    
                ),
            ),
        
    
)
