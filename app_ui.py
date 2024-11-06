from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.create_param import create_screen
from screens.screen_User import screen_User
from screens.screen3 import screen3
from screens.screen_Resultados import screenResult
from screens.screen_Validacion import screenValid
from screens.screen_desarollo import screenDesarollo
from screens.screen_produccion import screenProduccion
from screens.screen_in_sample import screenInSample
from screens.screen_login import screenLogin
app_ui = ui.page_fluid(
    ui.include_js(path="script.js", method="link"),
    ui.include_css(path="screens/project_root/estyle.css", method="link"),
    ui.navset_hidden(
        ui.nav_panel("Screen_Login", screenLogin),
        ui.nav_panel("Screen_User", screen_User),
        #ui.nav_panel("Screen_1", screen1),
        #ui.nav_panel("Screen_valid", screenValid),
        ui.nav_panel("Screen_Porduccion", screenProduccion),
        #ui.nav_panel("Screen_Desarollo", screenDesarollo),
        #ui.nav_panel("Screen_3", screen3),
        #ui.nav_panel("Screen_Resultados", screenResult),
        #ui.nav_panel("screen_in_sample", screenInSample)
    )
)
