from shiny import App, ui, reactive
from screens.screen_User import screen_User
from screens.screen_login import screenLogin
from screens.screen_config import screen_config


app_ui = ui.page_fluid(
    ui.include_js(path="script.js", method="link"),
    ui.include_css(path="screens/project_root/estyle.css", method="link"),
    ui.navset_hidden(
        #ui.nav_panel("Screen_Login", screenLogin),
        ui.nav_panel("Screen_User", screen_User),
        ui.nav_panel("screen_config", screen_config),
    )
)


app_login = ui.page_fluid(
    ui.include_js(path="script.js", method="link"),
    ui.include_css(path="screens/project_root/estyle.css", method="link"),
    ui.navset_hidden(
        ui.nav_panel("Screen_Login", screenLogin),
    )
)

