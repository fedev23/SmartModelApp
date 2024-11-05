from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.create_param import create_screen
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils import crear_card_con_input_seleccionador_V2, crear_card_con_input_numeric_2, crear_card_con_input_seleccionador
from global_names import global_name_desarrollo
from clases.global_session import global_session
from global_var import global_data_loader_manager


user_id = global_session.obtener_id()
json_loader = LoadJson(user_id=user_id)
previous_values = json_loader.load_json()
nombre_proyecto = global_user_proyecto

name_suffix = "desarrollo"
CHOICES = {
    "tipo": [",", '\\t', "' '", ";", "|"],
}

data_loader = global_data_loader_manager.get_loader(name_suffix)

screenDesarollo = ui.page_fluid(
    ui.div(
        ui.input_action_button("volver_etapas_desde_desarrollo", "SmartModeling", class_="logo-button")),
    ui.div(
        ui.output_ui("conten_nav")
    ),
    # ui.h3(ui.output_text("nombre_proyecto")),
    ui.div(
        ui.h3(f"{global_name_desarrollo}",  class_="custom-title"),
        # ui.h3("Modelo desarrollo", class_="custom-title"),
        ui.tags.div(ui.column(12, ui.input_select(
            "number_choice",
            "Selecciona un número de columnas de dataset",
            choices=[str(i) for i in range(5, 26)],
            width="100%",  # Genera una lista de opciones del 1 al 25
        ),
            )),

        ui.h4("Dataset"),
        ui.column(12, ui.input_file("file_desarollo", "Seleccion de archivo CSV o TXT",
                  button_label='Cargar archivo', placeholder='Buscar el archivo', accept=[".csv", ".txt"], width="100%")),
        ui.output_text_verbatim("error"),
        ui.output_text_verbatim("error_proyecto"),

        ui.div(
            ui.card(
                ui.card_header(f"Datos de {name_suffix}"),
                ui.output_data_frame(f"summary_data_{name_suffix}"),
            ),
        ),
        ui.h3(f"Parámetros de {name_suffix}", fillable=True),

    ),
    ui.div(
        ui.output_ui(f"acordeon_columnas_{name_suffix}"),
        ui.card(
            ui.row(
                ui.row(
                    # crear_card_con_input_seleccionador("column_select", "Selecciona Columnas", "action_link", icon="gear"),
                    crear_card_con_input_seleccionador("par_ids", "Columnas identificadora:", "help_columnas_id", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")),
                    crear_card_con_input_numeric_2(f"par_split", "Training and Testing", "help_training_testing", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"), previous_values, default_value=0, min_value=0, max_value=2, step=0.01),
                    crear_card_con_input_seleccionador("par_target", "Columna Target", "help_target_col", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"))

                ),
                ui.row(
                    crear_card_con_input_seleccionador(f"cols_forzadas_a_predictoras", "Variables forzada a variables candidatas", "help_vars_forzadas", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")),
                    crear_card_con_input_seleccionador(f"cols_forzadas_a_cat", "Columnas forzadas a categorías", "help_cols_forzadas_a_cat", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")),
                    crear_card_con_input_seleccionador(f"par_var_grupo",  "Define grupos para evaluar las candidatas", "help_par_var_grupo", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"))
                ),
                ui.row(
                    crear_card_con_input_seleccionador_V2("cols_nulos_adic", "Lista de variables y códigos de nulos", "help_nulos_adic", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")),
                    crear_card_con_input_numeric_2(f"par_cor_show", "Mostrar variables por alta correlación:", "help_par_cor_show", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"), previous_values, default_value=0, min_value=0, max_value=1, step=0.01),
                    crear_card_con_input_numeric_2(f"par_iv", "Límite para descartar variables por bajo IV", "help_iv", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"), previous_values, default_value=3, min_value=0.5, max_value=10, step=0.1),
                ),
                ui.row(
                    crear_card_con_input_seleccionador_V2(f"cols_no_predictoras", "Columnas excluidas del modelo", "help_cols_no_predictoras", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px")),
                    crear_card_con_input_numeric_2(f"par_cor", "Descartar variables por alta correlación", "help_par_cor", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"), previous_values, default_value=3, min_value=0.5, max_value=10, step=0.1),
                    crear_card_con_input_numeric_2(f"par_minpts1", "Casos mínimos de bin de primera etapa", "help_minpts", ui.tags.i(
                        class_="fa fa-question-circle-o", style="font-size:24px"), previous_values, default_value=3, min_value=0.5, max_value=10, step=0.1)
                ),
                ui.div(
                    ui.output_ui(f"error_{name_suffix}"),
                ),
                # class_="fixed-size"
            ),
        ),
        ui.output_text_verbatim(f"param_validation_3_{name_suffix}"),
        # class_="custom-column"
    ),


    ui.row(
        ui.column(12, ui.output_text_verbatim("file_status_desarollo")),
        ui.output_ui("update_action_button"),
        ui.output_ui("screen_content_desarollo"),
    ),


)
