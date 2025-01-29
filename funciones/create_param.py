from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.utils import crear_card_con_input_seleccionador, crear_card_con_input_numeric_2, crear_card_con_input_seleccionador_V3
from faicons import icon_svg
from global_var import global_data_loader_manager
from clases.global_session import global_session
data_loader = global_data_loader_manager.get_loader("desarrollo")


def create_screen(name_suffix):
    # Obtener los valores previos para este name_suffix o usar un valor predeterminado
    # values = previous_values
    return ui.page_fluid(
        ui.output_ui(f"mostrarModels_{name_suffix}"),
        ui.div(
            ui.row(
                ui.input_text("delimiter_desarollo", ""),
                ui.input_text("proyecto_nombre", ""),

                # Fila 1
                crear_card_con_input_numeric_2(
                    input_id="par_discret",
                    input_label="",
                    action_link_id="help_discret",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=1,
                    min_value=1,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_nbins1",
                    input_label="",
                    action_link_id="help_nbins1",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=100,
                    min_value=100,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_nbins2",
                    input_label="",
                    action_link_id="help_nbins2",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=20,
                    min_value=20,
                    max_value=1000,
                    step=0.01
                )
            ),
            ui.row(
                # Fila 2
                crear_card_con_input_numeric_2(
                    input_id="par_maxlevels",
                    input_label="",
                    action_link_id="help_maxlevels",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=50,
                    min_value=50,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_conf_level",
                    input_label="Límite para descartar variables por test de Chi-Sq en Forward",
                    action_link_id="help_minbinq",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=0.1,
                    min_value=0,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    # --> FUERON QUITADOS RMPLAZAR POR LOS OTROS nuevos par_conf_level
                    input_id="par_minpts_nulos",
                    input_label="Nro. de casos mínimos para asignar WoE a nulos",
                    action_link_id="help_minbinw",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=200,
                    min_value=0,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_minpts2",
                    input_label="Nro. de casos mínimos de cada bin de segunda etapa",
                    action_link_id="help_par_minpts2",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=400,
                    min_value=400,
                    max_value=1000,
                    step=0.01
                ),
                crear_card_con_input_seleccionador(
                    input_id="par_weight",
                    input_label="aa",
                    action_link_id="help_par_weight",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px")
                )
            ),
            ui.row(
                # Fila 3
                crear_card_con_input_numeric_2(
                    input_id="par_iv_cuantiles_gb_min",
                    input_label="",
                    action_link_id="help_iv_cuantiles",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=100,
                    min_value=100,
                    max_value=10000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_iv_tot_min",
                    input_label="",
                    action_link_id="help_iv_tot",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=500,
                    min_value=500,
                    max_value=2000,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_iv_tot_gb_min",
                    input_label="",
                    action_link_id="help_iv_tot_gb",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=200,
                    min_value=200,
                    max_value=1200,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_minpts_cat",
                    input_label="Nro. de casos mínimos de cada bin de la discretización de categorícas",
                    action_link_id="help_par_minpts_cat",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=150,
                    min_value=150,
                    max_value=1500,
                    step=0.01
                ),
                crear_card_con_input_numeric_2(
                    input_id="par_perf_bins",
                    input_label="Nro. de casos mínimos de cada bin de la discretización de categorícas",
                    action_link_id="help_par_perf_bins",
                    icon=ui.tags.i(class_="fa fa-question-circle-o",
                                   style="font-size:24px"),
                    default_value=20,
                    min_value=20,
                    max_value=200,
                    step=0.01
                ),
                ui.column(
                    4,
                    ui.row(
                        ui.card(
                            ui.card_header(
                                ui.row(
                                    ui.column(10, "Tabla de Segmentos"),
                                    ui.column(
                                        2,
                                        ui.input_action_link(
                                            "help_segmentos",
                                            ui.tags.i(
                                                class_="fa fa-question-circle-o", style="font-size:24px")
                                        )
                                    )
                                )
                            ),
                            ui.output_data_frame("par_rango_segmentos"),
                            class_="custom-card"
                        )
                    )
                ),
                crear_card_con_input_seleccionador_V3(
                    "par_vars_segmento", "Variables para reportes por Segmento", "vars_segmento",
                    ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")
                ),

                ui.div(ui.row(
                    crear_card_con_input_numeric_2(
                        input_id="par_times",
                        input_label="Submuestras para bootstrap",
                        action_link_id="times_sub",
                        icon=ui.tags.i(
                            class_="fa fa-question-circle-o", style="font-size:24px"),
                        default_value=25,
                        min_value=25,
                        max_value=2,
                        step=0.01
                    ),

                    crear_card_con_input_numeric_2(
                        input_id="par_cant_reportes",
                        input_label="Cantidad de reportes",
                        action_link_id="cant_reportes",
                        icon=ui.tags.i(
                            class_="fa fa-question-circle-o", style="font-size:24px"),
                        default_value=100,
                        min_value=100,
                        max_value=2,
                        step=0.01
                    ),


                    # style="display: flex; justify-content: space-around; align-items: center;"  # Estilo para mantener todo alineado
                ),

                ),

            ),
            class_="hidden-inputs"
        ),
    )
