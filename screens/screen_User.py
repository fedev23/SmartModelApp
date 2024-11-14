from shiny import ui
from funciones.funciones_user import show_selected_project_card
from shiny import App, ui, reactive
from screens.screen3 import screen3
from screens.screen_Resultados import screenResult
from screens.screen_Validacion import screenValid
from screens.screen_desarollo import screenDesarollo
from screens.screen_produccion import screenProduccion
from screens.screen_in_sample import screenInSample
from screens.screen_login import screenLogin
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
from clases.class_resultado import ResultadoClassPrueba
from screens.screen_desarollo import screenDesarollo


screen_User = ui.page_fluid(
    ui.tags.button("SmartModeling", class_="logo-button"),
    ui.output_ui("create_user_menu"),
    ui.tags.div(
            ui.card(
                    ui.output_ui("devolver_acordeon"),
                ),
            
            
        id="module_container",
    ),
    ui.output_ui("create_sidebar"),
    ui.output_ui("despligue_menu"),
    ui.navset_card_tab(  # Usa un contenedor de navegación adecuado
        ui.nav_panel(f"{global_name_desarrollo}", screenDesarollo),
        ui.nav_panel(f"{global_name_in_Sample}", screenInSample),
        ui.nav_panel(f"{global_name_out_of_Sample}", screenValid),
    ),
)