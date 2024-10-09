from shiny import App, ui, reactive
from global_names import global_name_out_of_Sample

# Opciones para los tipos de delimitador disponibles
CHOICES = {
    "tipo": [",", '\\t', "' '", ";", "|"],
}

# Definición de la pantalla de validación
screenValid = ui.page_fluid(
    # Contenedor para el botón de regreso
    ui.div(
        ui.input_action_button("volver_validacion", "SmartModel", class_="logo-button"),
    ),
    ui.output_ui("nav_out_to_sample"),
    # Contenedor para el contenido principal
    ui.div(
        ui.h3(f"{global_name_out_of_Sample}", class_="custom-title"),  # Título principal
        ui.h4("Dataset"),  # Subtítulo
        ui.column(12, 
            ui.input_file("file_validation", "Seleccion de archivo CSV o TXT", 
                button_label='Cargar archivo', 
                placeholder='Buscar el archivo', 
                accept=[".csv", ".txt"], 
                width="100%")  # Input para carga de archivos CSV o TXT
        ),
        ui.column(12, 
            ui.input_select("delimiter_validacion_out_to", "Tipo de delimitador", 
                choices=CHOICES["tipo"], 
                width="100%")  # Input para seleccionar el delimitador
        ),
        # Tarjeta para mostrar datos de validación
        ui.card(
            ui.card_header("Datos de" " " f"{global_name_out_of_Sample}"),  # Encabezado de la tarjeta
            ui.output_data_frame("summary_data_validacion_out_to_sample"),  # Salida del DataFrame de resumen
            ui.output_text("error_in_validacion"),  # Salida UI adicional
        ),
    ),
)
