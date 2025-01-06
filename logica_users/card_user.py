from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module

from api import *
from clases.global_session import global_session

def user_ui(input: Inputs, output: Outputs, session: Session, name_suffix):

    @output
    @render.ui
    def devolver_acordeon():
        # Obtiene la lista actual de proyectos
        projects = global_session.get_proyectos_usuarios()

        if projects:
            project_options = {
                str(project['id']): project['name'] for project in projects
            }

            return ui.page_fluid(

    # Primera fila
    ui.row(
        # Primera columna
        ui.column(
            5,
            ui.div(
                ui.tags.span("Proyecto:", style="margin-right: 10px; font-weight: bold; width: 150px; display: inline-block;"),
                ui.input_select(
                    "project_select",
                    "",
                    project_options,
                    width="50%"
                ),
                ui.div(
                    ui.input_action_link(
                        f"start_{name_suffix}",
                        ui.tags.i(class_="fa fa-plus-circle fa-2x", style="color: #007bff;")
                    ),
                    ui.output_ui("project_card_container"),
                    class_="d-flex align-items-stretch gap-3 mb-3"
                ),
                class_="d-flex align-items-stretch gap-3 mb-3"
            ),
        ),

        # Segunda columna
        ui.column(
            5,
            ui.div(
                ui.tags.span("Versión:", style="margin-right: 10px; font-weight: bold; width: 150px; display: inline-block;"),
                ui.input_select(
                    "other_select",
                    "",
                    {"a": "a"},
                    width="50%"
                ),
                ui.div(
                    ui.input_action_link(
                        f"version_{name_suffix}",
                        ui.tags.i(class_="fa fa-plus-circle fa-2x", style="color: #007bff;")
                    ),
                    ui.output_ui("button_remove_versions"),
                    class_="d-flex align-items-stretch gap-3 mb-3"
                ),
                class_="d-flex align-items-stretch gap-3 mb-3"
            ),
        ),
    ),

    # Segunda fila
    ui.row(
    # Tercera columna
    ui.column(
        5,
        ui.div(
            # Etiqueta "Niveles & ScoreCards"
            ui.tags.span(
                "Niveles & ScoreCards:",
                style="margin-right: 10px; font-weight: bold; width: 150px; display: inline-block;"
            ),
            # Selector de versión
            ui.input_select(
                "version_selector",
                "",
                {"a": "a"},
                width="50%"
            ),
            # Botón de acción y output
            ui.div(
                ui.input_action_link(
                    "create_parameters",
                    ui.tags.i(
                        class_="fa fa-plus-circle fa-2x",
                        style="color: #007bff;"
                    )
                ),
                ui.output_ui("button_remove_versions_param"),
                class_="d-flex align-items-center gap-3 mb-3"
            ),
            class_="d-flex align-items-center gap-3 mb-3"
        ),
        
    ),
    ui.column(
            5,
            ui.div(
            ui.tags.span(
                "Archivo de desarrollo:",
                style="margin-right: 10px; font-weight: bold; width: 150px; display: inline-block;"
            ),
            ui.output_text_verbatim("show_data_Set_in_card_user", placeholder=False),
            #ui.output_ui("show_data_Set_in_card_user"),
            class_="d-flex align-items-center gap-3 mb-3"
        ),
        class_="d-flex align-items-center gap-3 mb-3"
        )
)

)
