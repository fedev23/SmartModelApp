from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from global_var import global_data_loader_manager
from faicons import icon_svg
from funciones.utils import crear_card_con_input, crear_card_con_input_numeric, crear_card_con_input_seleccionador
from global_names import global_name_in_Sample
from funciones.utils import crear_card_con_input_numeric, crear_card_con_input_seleccionador_V3, crear_card_con_input_numeric_2
data = reactive.Value()
data_loader = global_data_loader_manager.get_loader("desarrollo")


@reactive.Effect
def obtenerDf():
    data = data_loader.getDataset()
    return data


# Datos de la tabla
screenInSample = ui.page_fluid(
    ui.head_content(
        ui.tags.link(
            rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
    ),
    # ui.output_ui("menuInSample"),
    ui.output_ui("salida_error"),
    ui.div(
        ui.card(
            ui.card_header(f"{global_name_in_Sample}"),
            ui.output_data_frame("summary_data_validacion_in_sample"),
            ui.output_ui("mostrarOut_sample"),
            # ui.output_text("mostrar_mensaje_datos")
        ),
        ui.row(
            # Columna para el botón
            ui.column(
                # Ancho de la columna (puedes ajustarlo según sea necesario)
                6,
                ui.div(
                   ui.input_action_button(
                    "create_parameters",
                    f"+ Create version parameters {global_name_in_Sample}",
                    class_="btn btn-dark btn-sm me-2",
                    style="font-size: 15px; padding: 8px 10px;"
                ),
                   class_="d-flex justify-content-between",  
                )
                
            ),

            # Columna para el selector
            ui.column(
                6,
                ui.row(
                    ui.div(
                   ui.input_select(
                    "version_selector",
                    "", # Si no deseas mostrar un texto de etiqueta
                    {"a": "a"},
                    #style="font-size: 15px;"
                ),
                    ui.column(1, ui.HTML("<div style='width: 20px;'></div>")),
                    ui.output_ui("button_remove_versions_param"),  
                   class_="d-flex justify-content-center",  
                ),
                
            )   
        ),
                ),
                # Ancho de la columna (puedes ajustarlo según sea necesario)
                
        # ui.tags.hr(),
        ui.div(class_="mt-5"),

    ),
    ui.div(
        ui.div(
            ui.row(
                ui.column(4,
                          ui.row(
                              ui.card(
                                  ui.card_header(
                                      ui.row(
                                          # Texto a la izquierda
                                          ui.column(3, ui.HTML("<div style='width: 20px;'></div>")),
                                          ui.column(
                                              10, "Tabla de Niveles de Riesgo"),
                                          ui.column(2,
                                                    ui.input_action_link("help_niveles", ui.tags.i(
                                                        class_="fa fa-question-circle-o", style="font-size:24px")),
                                                    )
                                      ),
                                  ),
                                  ui.output_data_frame("par_rango_niveles"),
                                  class_="custom-card",
                                  style="margin-left: 30px;"
                              )
                          )
                          ),
                ui.column(3, ui.HTML("<div style='width: 20px;'></div>")),
                ui.column(4,
                          ui.row(
                              ui.card(
                                  ui.card_header(
                                      ui.row(
                                          # Texto a la izquierda
                                          ui.column(10, "Tabla de Reportes"),
                                          ui.column(2,
                                                    ui.input_action_link("help_rangos", ui.tags.i(
                                                        class_="fa fa-question-circle-o", style="font-size:24px")),
                                                    )
                                      ),
                                  ),
                                  ui.output_data_frame("par_rango_reportes"),
                                  class_="custom-card"
                              )
                          )
                          ),
                
                ui.div( ui.row(
                        crear_card_con_input_numeric_2(
                        input_id="par_times",
                        input_label="Submuestras para bootstrap",
                        action_link_id="times_sub",
                        icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                        min_value=0,
                        max_value=2,
                        step=0.01
                        ),

                        crear_card_con_input_numeric_2(
                        input_id="par_cant_reportes",
                        input_label="Cantidad de reportes",
                        action_link_id="cant_reportes",
                        icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                        min_value=0,
                        max_value=2,
                        step=0.01
                        ),
                                            crear_card_con_input_seleccionador_V3(
                            "par_vars_segmento", "Variables para reportes por Segmento", "vars_segmento",
                            ui.tags.i(
                                class_="fa fa-question-circle-o", style="font-size:24px")
                        ),

                        # style="display: flex; justify-content: space-around; align-items: center;"  # Estilo para mantener todo alineado
                    ),
 
    ),
               

            ),
        ),
        # class_="custom-card"

        ui.tags.hr(),


        ui.navset_card_underline(
            ui.nav_panel(
                "Ejecución",
                ui.output_ui("mostrar_fin_inSample"),
                ui.output_ui("card_in_sample"),
                ui.output_ui("open_in_sample"),
                # ui.output_ui("card_in_sample"),
                ui.output_ui("open_in_sample"),
                # ui.output_ui("descarga_in_sample"),
                ui.output_ui("busy_indicator_in_sample"),
                ui.output_text_verbatim("mostrar_in_sample"),
                value="in_sample"



            ),
            ui.nav_spacer(),
            ui.nav_panel(
                "Resultados Validación In sample",
                ui.div(
                    ui.card(
                        ui.column(4, ui.download_button(
                            "descargar_resultados_validacion", "Descargar Todos los reportes validacion")),
                        ui.output_ui("resultado_card_validacion_in_sample"), value="in_sample"
                    )
                )
            )
        )

    ),

)
