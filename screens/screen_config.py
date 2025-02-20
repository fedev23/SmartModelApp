
from shiny import ui

screen_config = ui.page_fluid(
    ui.div(
        ui.tags.button("SmartModeling", class_="logo-button"),
    ),
    ui.tags.div(
        ui.row(
            ui.card(
                ui.card_header("Panel de Configuración"),
                ui.input_action_link("go_to_principal", "Volver al menu principal."),
                ui.tags.details(
                    ui.tags.summary("Configuración de filas"),
                    ui.div(class_="mt-2"),
                    ui.input_numeric(
                        "number_choice",
                        "Ingrese un número de filas para ver en el dataset",
                        value=5
                    )
                ),
                ui.tags.details(
                    ui.tags.summary("Configuración de segmentación"),
                    ui.div(class_="mt-2"),
                    ui.input_numeric(
                        "min_value",
                        "Ingrese el valor mínimo para la configuración de segmentación",
                        value=3
                    ),
                    ui.input_numeric(
                        "max_value",
                        "Ingrese el valor máximo para la configuración de segmentación",
                        value=8
                    )
                ),
            )
        ),
    ),
    ui.row(
        ui.column(
            6,
            ui.input_action_button(
                "save_modal", "Guardar", class_="btn-primary"),
            ui.input_action_button(
                "close_modal", "No guardar", class_="btn-secondary")
        ),
    ),
    # Pie de página con botones de ayuda y soporte
    ui.div(
        ui.row(
            ui.column(
                6,
                ui.input_action_link("help_button", "Ayuda y Documentación", class_="btn-info")
            ),
            ui.column(
                6,
                ui.input_action_link("support_button", "Soporte", class_="btn-warning", style="float: right;"),
            ),
        ),
        style="padding: 10px; margin-top: 20px; background-color: #f8f8f8; border-top: 1px solid #ddd;"
    )
)
