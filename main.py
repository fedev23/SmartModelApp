from starlette.applications import Starlette
from starlette.routing import Mount, Route
from shiny import App, reactive
from app_ui import app_ui, app_login
from servers.server_validacion_scoring.outofSample import server_out_of_sample
from servers.server_desarrollo.server_desarollo import server_desarollo
from servers.server_validacion_scoring.server_produccion import server_produccion
from resultados import server_resul
from user import user_server    
from servers.server_niveles_scorcards.server_in_sample import server_in_sample
from auth.auth import server_login
from logica_users.config_versiones import versiones_config_server
from logica_users.extend_of_user import extend_user_server
from  logica_users.card_user import user_ui
from servers.server_niveles_scorcards.in_Sample_versions import in_sample_verions
from servers.server_validacion_scoring.logica_scoring_valid import logica_server_Validacion_scroing
from servers.parametros.niveles_Scorcards.parametros_ui import server_niveles_Scorcards
from servers.parametros.parametros_desarrollo.parametros_desarrollo import server_parametros_desarrollo
from api.session_api import  SessionAPI
from api.endpoints_user import *
from auth.log_out import server_log_out, logout_starlette_session
from auth.endpoints import Auth0LoginEndpoint
from starlette.middleware.cors import CORSMiddleware
from api.utils import *
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
from auth.validate import ValidateTokenEndpoint
from api.api_manager import *
from  api.middleware import AuthMiddleware
from api.login import LoginEndpoint, LoginStarletteSessionEndpoint, LoginPageEndpoint


# Define the Shiny server function
def create_server(input, output, session):
    server_parametros_desarrollo(input, output, session, 'desarrollo')
    server_log_out(input, output, session)
    #server_login(input, output, session),
    logica_server_Validacion_scroing(input, output, session, 'Scroring_out_of_sample')
    user_ui(input, output, session, 'user')
    versiones_config_server(input, output, session)
    in_sample_verions(input, output, session,"versiones_json")
    extend_user_server(input, output, session, "extend_user_server")
    server_desarollo(input, output, session, 'desarrollo')
    server_out_of_sample(input, output, session, 'validacion')
    server_produccion(input, output, session, 'produccion')
    server_niveles_Scorcards(input, output, session, 'in_sample')
    server_in_sample(input, output, session, 'in_sample')
    server_resul(input, output, session, 'resultados')
    user_server(input, output, session, 'user')

   

# Create the Shiny app
app_shiny = App(app_ui, create_server)


def screen_login(input, output, session):
    server_login(input, output, session),
    #server_redireccionamiento(input, output, session)
    
login = App(app_login, screen_login)

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
middleware = [
    Middleware(CORSMiddleware,
               allow_origins=["http://localhost:3000"],  # o ["*"] para debug
               allow_methods=["*"],
               allow_headers=["*"],
               allow_credentials=True),
    Middleware(SessionMiddleware, secret_key=secret_key, max_age=7200, https_only=False),
    Middleware(AuthMiddleware),
]   


# Define the routes for Starlette
routes = [
    #Route('/api/auth/login', Auth0LoginEndpoint, methods=["POST"]),
    Route('/api/user_files', DynamicStaticFileEndpoint, methods=["GET"]),
    Route('/login_clean', LoginPageEndpoint, methods=["GET"]),
    Route('/api/login', LoginEndpoint, methods=["POST"]),
    Route("/api/logout_starlette_session", logout_starlette_session, methods=["POST"]),
    Route('/api/login_starlette_session', LoginStarletteSessionEndpoint, methods=["POST"]),
    Route('/api/process_user_id', ProcessUserIDEndpoint, methods=["POST"]),
    Route('/api/session', SessionAPI, methods=["POST", "GET"]),
    Route('/api/validate_token', ValidateTokenEndpoint, methods=["POST"]),
    #Route("/api/check_auth", check_auth, methods=["GET"]),
    Mount('/shiny/', app=app_shiny),
    Mount('/login', app=login)
]
app = Starlette(routes=routes, middleware=middleware)
#app.add_middleware(ShinyAuthMiddleware) 
# run:
# uvicorn main:app --host 127.0.0.1 --port 3000 --reload
