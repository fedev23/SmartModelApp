from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from global_var import global_data_loader_manager
from faicons import icon_svg
from funciones.utils import crear_card_con_input, crear_card_con_input_numeric, crear_card_con_input_seleccionador
from global_names import global_name_in_Sample

data = reactive.Value()
data_loader = global_data_loader_manager.get_loader("desarrollo")

@reactive.Effect
def obtenerDf():
    data = data_loader.getDataset()
    return data

# Datos de la tabla
screenInSample = ui.page_fluid(
    ui.head_content(
        ui.tags.link(rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
    ),
    ui.div(
        ui.input_action_button("volver_inSample", "SmartModel", class_="logo-button"), 
    ),
    ui.output_ui("menuInSample"),
    ui.output_ui("salida_error"),
    ui.div(
        ui.h3(f"{global_name_in_Sample}", class_="custom-title"),
        ui.h4("Dataset"),  
    ),
    ui.div(
        ui.card(
            ui.card_header(f"{global_name_in_Sample}"),
            ui.output_data_frame("summary_data_validacion_in_sample"),
            ui.output_ui("mostrarOut_sample"),
            # ui.output_text("mostrar_mensaje_datos")
        ),
        ui.h3("Parametros" " " f"{global_name_in_Sample}"),
    ),
    ui.div(
        ui.card(
        ui.row(
            ui.column(4, 
                ui.row(
                    ui.card(
                        ui.card_header(
                            ui.row(
                                ui.column(10, "Tabla de Niveles de Riesgo"),  # Texto a la izquierda
                                ui.column(2, 
                                    ui.input_action_link("help_niveles", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                                )
                            ),
                        ),
                        ui.output_data_frame("par_rango_niveles"),
                         class_="custom-card"
                    )
                )
            ),
            ui.column(4, 
                ui.row(
                    ui.card(
                        ui.card_header(
                            ui.row(
                                ui.column(10, "Tabla de Segmentos"),  # Texto a la izquierda
                                ui.column(2, 
                                    ui.input_action_link("help_segmentos", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                                )
                            ),
                        ),
                        ui.output_data_frame("par_rango_segmentos"),
                         class_="custom-card"
                    )
                )
            ),
             ui.column(4, 
                ui.row(
                    ui.card(
                        ui.card_header(
                            ui.row(
                                ui.column(10, "Tabla de Reportes"),  # Texto a la izquierda
                                ui.column(2, 
                                    ui.input_action_link("help_rangos", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
                                )
                            ),
                        ),
                        ui.output_data_frame("par_rango_reportes"),
                         class_="custom-card"
                    )
                )
            ),
             ui.row(
            ui.column(12, ui.HTML("<div style='height: 30px;'></div>"))
        ),
        ui.row(
            crear_card_con_input_seleccionador("par_vars_segmento", "Variables para reportes por Segmento", "vars_segmento", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")),
            crear_card_con_input_numeric("par_times", "Submuestras para bootstrap", "times_sub", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), value=25),
            crear_card_con_input_numeric("par_cant_reportes", "Cantidad de reportes", "cant_reportes", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), value=100), 
            #ui.column(4, ui.input_text("par_vars_segmento", "Variables para reportes por Segmento")),
            #ui.column(4, ui.input_numeric("par_cant_reportes", "Cantidad de reportes", value=100)),
        ), 
            
        ),
        ),
         #class_="custom-card"
       
    )   
)
