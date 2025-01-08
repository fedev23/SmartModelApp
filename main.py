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
from logica_users.config_versiones import versiones_config_server
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
    versiones_config_server(input, output, session)
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

def validate_params(required_params, provided_params):
    """Valida que todos los parámetros requeridos estén presentes."""
    missing_params = [param for param in required_params if not provided_params.get(param)]
    if missing_params:
        return {"error": f"Missing required parameters: {', '.join(missing_params)}"}
    return None


def build_base_directory(user_id, id_proyecto, nombre_proyecto):
    return f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id}/proyecto_{id_proyecto}_{nombre_proyecto}"

def build_insample_folder(base_directory, id_version, nombre_version, id_version_insample, nombre_version_insample):
    return f"{base_directory}/version_{id_version}_{nombre_version}/version_parametros_{id_version_insample}_{nombre_version_insample}"




class ProcessUserIDEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        
        # Validar parámetros básicos
        required_params = ["user_id", "nombre_proyecto", "id_proyecto", "id_version", "nombre_version"]
        validation_error = validate_params(required_params, data)
        if validation_error:
            return JSONResponse(validation_error, status_code=400) 
        
        # Parámetros adicionales
        id_version_insample = data.get("id_version_insample")
        nombre_version_insample = data.get("nombre_version_insample")
        nombre_folder_validacion_scoring = data.get("nombre_folder_validacion_scoring")

        if id_version_insample and nombre_version_insample:
            message = (f"User ID {data['user_id']} with Project '{data['nombre_proyecto']}' (ID {data['id_proyecto']}) "
                       f"and Version '{data['nombre_version']}' (ID {data['id_version']}) and Insample Version "
                       f"'{nombre_version_insample}' (ID {id_version_insample}) processed successfully")
            if nombre_folder_validacion_scoring:
                message += f" for foldername {nombre_folder_validacion_scoring}"
            return JSONResponse({"message": message})

        return JSONResponse({"message": "Process completed successfully without insample parameters"})
        


class DynamicStaticFileEndpoint(HTTPEndpoint):
    async def get(self, request):
        user_id = request.query_params.get("user_id")
        nombre_proyecto = request.query_params.get("nombre_proyecto")
        id_proyecto = request.query_params.get("id_proyecto")
        id_version = request.query_params.get("id_version")
        nombre_version = request.query_params.get("nombre_version")
        file_name = request.query_params.get("file_name")
        id_version_insample = request.query_params.get("id_version_insample")
        nombre_version_insample = request.query_params.get("nombre_version_insample")
        nombre_folder_validacion_scoring = request.query_params.get("nombre_folder_validacion_scoring")

        # Validar parámetros obligatorios
        if not all([user_id, nombre_proyecto, id_proyecto, id_version, nombre_version, file_name]):
            return JSONResponse({"error": "Missing required parameters for path construction"}, status_code=400)

        file_name = unquote(file_name)

        # Ruta base común
        base_directory = build_base_directory(user_id, id_proyecto, nombre_proyecto)

        if id_version_insample and nombre_version_insample:
            # Ruta base para in-sample
            base_insample_folder = build_insample_folder(base_directory, id_version, nombre_version, id_version_insample, nombre_version_insample)
            print(f"Base in-sample folder: {base_insample_folder}")

            if nombre_folder_validacion_scoring:
                scoring_folder_path = os.path.join(base_insample_folder, nombre_folder_validacion_scoring, "Reportes")
                print(f"Scoring folder path (debug): {scoring_folder_path}")
                
                if os.path.isdir(scoring_folder_path):
                    user_directory = os.path.join(scoring_folder_path, file_name)
                    print(f"File path (debug): {user_directory}")
                else:
                    print(f"Scoring folder not found: {scoring_folder_path}")
                    return JSONResponse({"error": f"Folder for validation scoring not found: {scoring_folder_path}"}, status_code=404)
        else:
            # Ruta genérica
            user_directory = f"{base_directory}/version_{id_version}_{nombre_version}/Reportes/{file_name}"
            print(f"Generic user_directory: {user_directory}")

        # Verificar si el archivo existe
        if os.path.isfile(user_directory):
            print(f"Archivo encontrado: {user_directory}")
            return FileResponse(user_directory)
        else:
            print(f"Archivo no encontrado: {user_directory}")
            return JSONResponse({"error": f"File not found: {user_directory}"}, status_code=404)

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
