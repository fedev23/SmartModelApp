from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from global_var import global_data_loader_manager
from faicons import icon_svg
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
        ui.tags.link(
            rel="stylesheet", href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css")
    ),
    # ui.output_ui("menuInSample"),
    ui.output_ui("salida_error"),

    # Ancho de la columna (puedes ajustarlo según sea necesario)

    ui.div(
        ui.card(
            ui.card_header(f"{global_name_in_Sample}"),
            ui.output_data_frame("summary_data_validacion_in_sample"),
            ui.output_ui("mostrarOut_sample"),
            # ui.output_text("mostrar_mensaje_datos")
        ),
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
                                          ui.column(3, ui.HTML(
                                              "<div style='width: 20px;'></div>")),
                                          ui.column(
                                              10, "Tabla de Niveles de Riesgo"),
                                          ui.column(2,
                                                    ui.input_action_link("help_niveles", ui.tags.i(
                                                        class_="fa fa-question-circle-o", style="font-size:24px")),
                                                    ),
                                          
                                          ui.div(class_="mt-5"),
                                          ui.row(
                                              ui.column(4, ui.input_text(
                                                  "add_value", "", placeholder="Inserte un nombre de nivel")),
                                              ui.column(4, ui.input_text(
                                                  "add_regla", "", placeholder="Agregue un nivel de regla por ejemplo: 740>=")),
                                              ui.column(4, ui.input_text(
                                                  "add_tasa_malos", "", placeholder="Agregue una tasa de malos")),
                                              
                                            #ui.tags.hr(),
                                            ui.row(
                                                #ui.column(4, ui.output_ui("return_inser_values"),
                                                ui.column(4, ui.input_action_link("add_files_niveles_riesgo_2", "Insertar")),
                                                ui.column(4, ui.div()),
                                                ui.column(4, ui.input_action_link("eliminar_filas_par_rango_niveles", "Eliminar fila")),
                                                
                                            ),
                                            ),
                                      ),
                                  ),
                                  ui.output_data_frame("par_rango_niveles"),
                                  #ui.tags.hr(),
                                  #ui.input_action_link("eliminar_fila_niveles_riesgo", "Eliminar fila seleccionada"),
                                  #class_="custom-card",
                                  #style="margin-left: 30px;"
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
                                                    ),
                                      ),
                                      ui.column(
                                          6,
                                          ui.output_ui("selector"),
                                          ui.output_ui("insert"),
                                      )
                                  ),
                                  ui.output_data_frame("par_rango_reportes"),
                                  ui.output_ui("delete"),

                                  #class_="custom-card"
                              )
                          )
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
                f"Resultados {global_name_in_Sample}",
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
