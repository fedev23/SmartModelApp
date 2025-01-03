from shiny import ui

def create_lay():
    return  ui.card(
        ui.layout_sidebar(
            ui.sidebar("Left sidebar content", id="sidebar_left"),
            ui.output_text_verbatim("state_left"),
        )
    ),