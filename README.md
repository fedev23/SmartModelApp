import requests





vfrom starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from shiny import App, reactive
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
from clases.global_session import global_session
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

# Variable global para almacenar el ID del usuario
user_id_global = None

# Obtener el `user_id` desde la sesión y actualizar `user_id_global`
def get_user_id_from_session():
    @reactive.effect
    def enviar_session():
        if global_session.proceso.get():
            state = global_session.session_state.get()
            if state["is_logged_in"]:
                user_id = state["id"].replace('|', '_')
                global user_id_global
                user_id_global = user_id
                logging.debug(f"[get_user_id_from_session] user_id_global asignado: {user_id_global}")
                return user_id

# Middleware dinámico para actualizar el directorio estático
class DynamicStaticMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        if request.url.path.startswith("/static"):
            if user_id_global:
                user_directory = f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes"
                if os.path.exists(user_directory):
                    static_app = StaticFiles(directory=user_directory, html=True)
                    try:
                        response = await static_app(request.scope, request.receive, request._send)
                        return response
                    except Exception as e:
                        logging.error(f"Error al servir archivo estático: {e}")
                else:
                    logging.warning(f"Directorio estático no encontrado para el usuario {user_id_global}")
            return await call_next(request)
        return await call_next(request)

# Función para crear el servidor de Shiny
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
    
    get_user_id_from_session()

# Crear la aplicación Shiny
app_shiny = App(app_ui, create_server)

# Definir las rutas de Starlette
routes = [
    Mount('/shiny', app=app_shiny),
    Mount('/static', app=StaticFiles(directory="/mnt/c/Users/fvillanueva/flask_prueba/static", html=True))  # Ruta predeterminada
]

# Crear la aplicación principal de Starlette y añadir el middleware
app = Starlette(routes=routes)  
app.add_middleware(DynamicStaticMiddleware)

logging.debug("Aplicación Starlette iniciada con middleware dinámico para archivos estáticos.")
