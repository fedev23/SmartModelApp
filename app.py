from shiny import App, run_app
from app_ui import app_ui
from outofSample import server_out_of_sample
from validacion_param.parametros_desarrollo import server_parametros_desarrollo
from modelo import server_modelos
from server_desarollo import server_desarollo
from server_produccion import server_produccion
from resultados import server_resul
from user import user_server    
from servers.server_in_sample import server_in_sample
from auth.auth import server_login



def create_server(input, output, session):
    server_parametros_desarrollo(input, output, session, 'desarrollo')
    server_login(input, output, session)
    server_desarollo(input, output, session, 'desarrollo')
    server_out_of_sample(input, output, session, 'validacion')
    server_produccion(input, output, session, 'produccion')
    server_in_sample(input, output, session, 'in_sample')
    server_modelos(input, output, session, 'modelo')
    server_resul(input, output, session, 'resultados')
    user_server(input, output, session, 'user')

# Crear la instancia de la aplicación Shiny
app = App(app_ui, create_server)

if __name__ == "__main__":
    # Ejecución de la aplicación usando run_app
    run_app(app='app:app', host='127.0.0.1', port=8000, launch_browser=True)
    
