from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.utils import crear_card_con_input_seleccionador, crear_card_con_input_numeric_2
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
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
             crear_card_con_input_numeric_2(
                input_id="par_nbins1",
                input_label="",
                action_link_id="help_nbins1",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_nbins2",
                input_label="",
                action_link_id="help_nbins2",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            )
        ),
        ui.row(
            # Fila 2
            crear_card_con_input_numeric_2(
                input_id="par_maxlevels",
                input_label="",
                action_link_id="help_maxlevels",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_limit_by_minbinq",
                input_label="",
                action_link_id="help_minbinq",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_limit_by_minbinw",
                input_label="",
                action_link_id="help_minbinw",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_minpts2",
                input_label="Nro. de casos mínimos de cada bin de segunda etapa",
                action_link_id="help_par_minpts2",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_seleccionador(
                input_id="par_weight",
                input_label="aa",
                action_link_id="help_par_weight",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
            )
        ),
        ui.row(
            # Fila 3
            crear_card_con_input_numeric_2(
                input_id="par_iv_cuantiles_gb_min",
                input_label="",
                action_link_id="help_iv_cuantiles",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_iv_tot_min",
                input_label="",
                action_link_id="help_iv_tot",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_iv_tot_gb_min",
                input_label="",
                action_link_id="help_iv_tot_gb",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_minpts_cat",
                input_label="Nro. de casos mínimos de cada bin de la discretización de categorícas",
                action_link_id="help_par_minpts_cat",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
                step=0.01
            ),
            crear_card_con_input_numeric_2(
                input_id="par_perf_bins",
                input_label="Nro. de casos mínimos de cada bin de la discretización de categorícas",
                action_link_id="help_par_perf_bins",
                icon=ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"),
                min_value=0,
                max_value=2,
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
                                        ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px")
                                    )
                                )
                            )
                        ),
                        ui.output_data_frame("par_rango_segmentos"),
                        class_="custom-card"
                    )
                )
            )
        ),
        class_="hidden-inputs"
    ),
)
