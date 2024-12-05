from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from shiny import App, reactive
import os 
from starlette.responses import FileResponse, JSONResponse
from app_ui import app_ui
from servers.server_validacion_scoring.outofSample import server_out_of_sample
from modelo import server_modelos
from servers.server_desarrollo.server_desarollo import server_desarollo
from servers.server_validacion_scoring.server_produccion import server_produccion
from resultados import server_resul
from user import user_server    
from servers.server_niveles_scorcards.server_in_sample import server_in_sample
from auth.auth import server_login
from logica_users.extend_of_user import extend_user_server
from  logica_users.card_user import user_ui
from servers.server_niveles_scorcards.in_Sample_versions import in_sample_verions
from servers.server_validacion_scoring.logica_scoring_valid import logica_server_Validacion_scroing
from servers.parametros.niveles_Scorcards.parametros_ui import server_niveles_Scorcards
from servers.parametros.parametros_desarrollo.parametros_desarrollo import server_parametros_desarrollo
from urllib.parse import unquote


# Define the Shiny server function
def create_server(input, output, session):
    server_parametros_desarrollo(input, output, session, 'desarrollo')
    server_login(input, output, session),
    logica_server_Validacion_scroing(input, output, session, 'Scroring_out_of_sample')
    user_ui(input, output, session, 'user'),
    in_sample_verions(input, output, session,"versiones_json")
    extend_user_server(input, output, session, "extend_user_server")
    server_desarollo(input, output, session, 'desarrollo')
    server_out_of_sample(input, output, session, 'validacion')
    server_produccion(input, output, session, 'produccion')
    server_niveles_Scorcards(input, output, session, 'in_sample')
    server_in_sample(input, output, session, 'in_sample')
    server_modelos(input, output, session, 'modelo')
    server_resul(input, output, session, 'resultados')
    user_server(input, output, session, 'user')

   

# Create the Shiny app
app_shiny = App(app_ui, create_server)


class ProcessUserIDEndpoint(HTTPEndpoint):
    async def post(self, request):
        # Parsear el cuerpo JSON de la solicitud
        data = await request.json()
        user_id = data.get("user_id")
        nombre_proyecto = data.get("nombre_proyecto")
        id_proyecto = data.get("id_proyecto")
        id_version = data.get("id_version")
        nombre_version = data.get("nombre_version")

        # Validar si todos los parámetros están presentes
        if user_id and nombre_proyecto and id_proyecto and id_version and nombre_version:
            return JSONResponse({
                "message": f"User ID {user_id} with Project '{nombre_proyecto}' (ID {id_proyecto}) "
                           f"and Version '{nombre_version}' (ID {id_version}) processed successfully"
            })
        else:
            return JSONResponse({
                "error": "Missing required parameters"
            }, status_code=400)        
        

class DynamicStaticFileEndpoint(HTTPEndpoint):
    async def get(self, request):
        user_id = request.query_params.get("user_id")
        nombre_proyecto = request.query_params.get("nombre_proyecto")
        id_proyecto = request.query_params.get("id_proyecto")
        id_version = request.query_params.get("id_version")
        nombre_version = request.query_params.get("nombre_version")
        file_name = request.query_params.get("file_name")

        
        file_name = unquote(file_name)

        if user_id and nombre_proyecto and id_proyecto and id_version and nombre_version and file_name:
            user_directory = (
                f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id}/proyecto_{id_proyecto}_{nombre_proyecto}/version_{id_version}_{nombre_version}/Reportes/{file_name}"
            )
            #full_path = os.path.join(user_directory, file_name)
            #print(full_path, "ESTOY VIENDO EL FULL PATH")
            if os.path.isfile(user_directory):
                return FileResponse(user_directory)
            else:
                return JSONResponse({"error": "File not found"}, status_code=404)
        else:
            return JSONResponse({"error": "Missing required parameters"}, status_code=400)

# Define the routes for Starlette
routes = [
    Route('/api/user_files', DynamicStaticFileEndpoint, methods=["GET"]),
    Route('/api/process_user_id', ProcessUserIDEndpoint, methods=["POST"]),
    Mount('/shiny', app=app_shiny),
]
#C:\Users\fvillanueva\Desktop\SmartModel_new_version\new_version_new\Automat\datos_salida_auth0_670fc1b2ead82aaae5c1e9ba\proyecto_57_Proyecto_prueba_De_Datos\version_30_Inicial\Reportes
# Create the main Starlette app with the defined routes
app = Starlette(routes=routes)

# run:
# uvicorn main:app --host 127.0.0.1 --port 3000 --reload
