from shiny import ui, render, reactive

screenLogin = ui.page_fluid(  # Incluimos los estilos
    ui.div(
        ui.div(
            ui.card(
                ui.input_text("username", "Correo electrónico:"),
                ui.input_password("password", "Contraseña:"),
                ui.input_action_button("login_button", "Login"),
                ui.output_text_verbatim("login_message"),
                class_="card-custom"
            ),
            class_="center-card"
        )
    )
)