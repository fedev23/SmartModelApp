from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from shiny import App, reactive
import os 
from starlette.responses import FileResponse, JSONResponse
from app_ui import app_ui
from outofSample import server_out_of_sample
from parametros.parametros_desarrollo import server_parametros_desarrollo
from parametros.niveles_Scorcards.parametros_ui import server_niveles_Scorcards
from modelo import server_modelos
from server_desarollo import server_desarollo
from server_produccion import server_produccion
from resultados import server_resul
from user import user_server    
from servers.server_in_sample import server_in_sample
from auth.auth import server_login
from logica_users.extend_of_user import extend_user_server
from  logica_users.card_user import user_ui
from servers.in_Sample_versions import in_sample_verions
from servers.logica_scoring_valid import logica_server_Validacion_scroing



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
    server_in_sample(input, output, session, 'in_sample')
    server_niveles_Scorcards(input, output, session, 'in_sample')
    server_modelos(input, output, session, 'modelo')
    server_resul(input, output, session, 'resultados')
    user_server(input, output, session, 'user')

   

# Create the Shiny app
app_shiny = App(app_ui, create_server)


class ProcessUserIDEndpoint(HTTPEndpoint):
    async def get(self, request):
        print("Received request")
        user_id = request.query_params.get("user_id")  # Obtiene el user_id de los parametros de consulta
        print(f"User ID: {user_id}")
        if user_id:
            return JSONResponse({"message": f"User ID {user_id} processed successfully"})
        else:
            return JSONResponse({"error": "User ID not provided"}, status_code=400)
        
        
class DynamicStaticFileEndpoint(HTTPEndpoint):
    async def get(self, request):
        user_id = request.query_params.get("user_id")  # Obtener el user_id de los parámetros de consulta
        if user_id:
            # Construir el directorio del usuario
            user_directory = f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id}/Reportes"
            
            # Obtener el nombre del archivo solicitado
            file_path = request.path_params["file_name"]
            full_path = os.path.join(user_directory, file_path)
            
            # Comprobar si el archivo existe
            if os.path.isfile(full_path):
                return FileResponse(full_path)
            else:
                return JSONResponse({"error": "File not found"}, status_code=404)
        else:
            return JSONResponse({"error": "User ID not provided"}, status_code=400)


# Define the routes for Starlette
routes = [
    Route('/api/user_files/{file_name}', DynamicStaticFileEndpoint), 
    #http://127.0.0.1:3000/api/user_files/{file_name}?user_id=12345
    Route('/api/process_user_id', ProcessUserIDEndpoint),
    Mount('/shiny', app=app_shiny),
   
]

# Create the main Starlette app with the defined routes
app = Starlette(routes=routes)

# run:
# uvicorn main:app --host 127.0.0.1 --port 3000 --reload
