from starlette.responses import JSONResponse, PlainTextResponse
from starlette.endpoints import HTTPEndpoint
import os 
from starlette.responses import FileResponse, JSONResponse
from urllib.parse import unquote
from api.utils.validate import validate_params
from api.utils.paths import build_base_directory, build_insample_folder
from starlette.requests import ClientDisconnect

class ProcessUserIDEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        try:
            data = await request.json()
        except ClientDisconnect:
            return JSONResponse({"error": "Cliente desconectado antes de enviar los datos"}, status_code=400)
        except Exception as e:
            return JSONResponse({"error": f"Error al procesar JSON: {str(e)}"}, status_code=400)
        
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
        user_directory = None  # Inicializamos como None para cubrir todos los casos

        # Caso 1: in-sample
        if id_version_insample and nombre_version_insample:
            base_insample_folder = build_insample_folder(
                base_directory, id_version, nombre_version, id_version_insample, nombre_version_insample
            )
            print(f"base_insample_folder: {base_insample_folder}")

            # Caso 1.1: scoring dentro de in-sample
            if nombre_folder_validacion_scoring:
                scoring_folder_path = os.path.join(base_insample_folder, nombre_folder_validacion_scoring, "Reportes")
                print(f"Scoring folder path: {scoring_folder_path}")

                if os.path.isdir(scoring_folder_path):
                    user_directory = os.path.join(scoring_folder_path, file_name)
                    print(f"File path for in-sample scoring: {user_directory}")
                else:
                    return JSONResponse({"error": f"Scoring folder not found: {scoring_folder_path}"}, status_code=404)
            else:
                # Caso 1.2: in-sample sin scoring
                user_directory = os.path.join(base_insample_folder, "Reportes", file_name)
                print(f"File path for in-sample: {user_directory}")

        # Caso 2: ruta genérica (si no se cumple in-sample)
        if user_directory is None:
            user_directory = os.path.join(base_directory, f"version_{id_version}_{nombre_version}", "Reportes", file_name)
            print(f"Generic user_directory: {user_directory}")

        # Verificar si el archivo existe
        if os.path.isfile(user_directory):
            print(f"Archivo encontrado: {user_directory}")
            return FileResponse(user_directory)
        else:
            print(f"Archivo no encontrado: {user_directory}")
            return JSONResponse({"error": f"File not found: {user_directory}"}, status_code=404)
        



