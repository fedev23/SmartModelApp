from shiny import ui
from funciones.funciones_user import show_selected_project_card

screen_User = ui.page_fluid(
    ui.tags.button("SmartModeling", class_="logo-button"),
    ui.output_ui("create_user_menu"),
    ui.tags.div(
    ui.accordion(
        ui.accordion_panel(
            "Proyectos:",
            ui.card(
                ui.output_ui("devolver_acordeon"),
                # sfull_screen=True,
            ),
        ),
        open=False,
    ),
    id="module_container",
    ),
    
    ui.output_ui("create_sidebar"),
    # ui.h3("Tarjeta de Usuario", fillable=True)
    ui.output_ui("despligue_menu"),
),
