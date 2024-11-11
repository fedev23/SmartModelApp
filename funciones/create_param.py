from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.utils import crear_card_con_input_seleccionador, crear_card_con_input_numeric_2
from faicons import icon_svg
from global_var import global_data_loader_manager
from clases.global_session import global_session 
data_loader = global_data_loader_manager.get_loader("desarrollo")

user_id = global_session.obtener_id()
json_loader = LoadJson(user_id=user_id)
values = json_loader.load_json()

def create_screen(name_suffix):
    # Obtener los valores previos para este name_suffix o usar un valor predeterminado
    #values = previous_values
    return ui.page_fluid(
        ui.output_ui(f"mostrarModels_{name_suffix}"),
        ui.div(
            ui.row(
                ui.input_text("delimiter_desarollo", ""),
                ui.input_text("proyecto_nombre", ""),
                crear_card_con_input_numeric_2(f"par_discret", "", "help_discret", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=1,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_nbins1", "", "help_nbins1", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values,default_value=100),
                crear_card_con_input_numeric_2(f"par_nbins2", "", "help_nbins2", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=20)
            ),
            ui.row(
                crear_card_con_input_numeric_2(f"par_maxlevels", "", "help_maxlevels", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=50,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_limit_by_minbinq", "", "help_minbinq", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=1,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_limit_by_minbinw", "", "help_minbinw", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=1),
                crear_card_con_input_numeric_2(f"par_minpts2", "Nro. de casos mínimos de cada bin de segunda etapa", "help_par_minpts2", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=400,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_seleccionador(f"par_weight",  "aa", "help_par_weight",ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"))
                
            ),
            ui.row(
                crear_card_con_input_numeric_2(f"par_iv_cuantiles_gb_min", "", "help_iv_cuantiles", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=100,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_iv_tot_min", "", "help_iv_tot", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=500,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_iv_tot_gb_min", "", "help_iv_tot_gb", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=200,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_minpts_cat", "Nro. de casos mínimos de cada bin de la discretización de categorícas", "help_par_minpts_cat", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=400,  min_value=0, max_value=2, step=0.01),
                crear_card_con_input_numeric_2(f"par_perf_bins", "Nro. de casos mínimos de cada bin de la discretización de categorícas", "help_par_perf_bins", ui.tags.i(class_="fa fa-question-circle-o", style="font-size:24px"), values, default_value=20,  min_value=0, max_value=2, step=0.01)
            ),
            class_="hidden-inputs"
        ),
    )
