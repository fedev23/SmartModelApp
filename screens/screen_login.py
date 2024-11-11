from shiny import ui, render, reactive

screenLogin = ui.page_fluid(  # Incluimos los estilos
    ui.div(
        ui.input_action_button(
            "boton_login", "SmartModeling", class_="logo-button"),
        ui.div(
            ui.card(
                ui.input_text("username", "Correo electrónico:", value=""),
                ui.input_password("password", "Contraseña:"),
                ui.input_action_button("login_button", "Login"),
                ui.div(
                    ui.output_text("login_message"),
                ),
                class_="card-custom"
            ),
            class_="center-card"
        )
    )
)
