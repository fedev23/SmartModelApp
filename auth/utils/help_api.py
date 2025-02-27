import requests
import httpx

def procesar_starlette_api(user_id, nombre_proyecto, id_proyecto, id_version, nombre_version):
    """Envía datos al API de Starlette y procesa la respuesta."""
    url = "http://127.0.0.1:3000/api/process_user_id"
    data = {
        "user_id": user_id,
        "nombre_proyecto": nombre_proyecto,
        "id_proyecto": id_proyecto,
        "id_version": id_version,
        "nombre_version": nombre_version
    }

    print("Datos enviados al servidor:", data)
    try:
        # Enviar datos como JSON en una solicitud POST
        starlette_response = requests.post(url, json=data, timeout=5)  # Tiempo de espera de 1 segundo
        if starlette_response.status_code == 200:
            print("Respuesta de la API de Starlette:", starlette_response.json())
            return starlette_response.json()  # Retorna la respuesta en formato JSON
        else:
            print("Error en la API de Starlette:", starlette_response.text)
            return {"error": starlette_response.text}  # Retorna el error como diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud a la API de Starlette: {e}")
        return {"error": str(e)}  # Retorna el error de la excepción



def procesar_starlette_api_insample(user_id, nombre_proyecto, id_proyecto, id_version, nombre_version, id_version_insample, nombre_version_insample ):
        """Envía datos al API de Starlette para procesar 'in sample' y procesa la respuesta."""
        url = "http://127.0.0.1:3000/api/process_user_id"  # Endpoint específico para in sample
        data = {
            "user_id": user_id,
            "nombre_proyecto": nombre_proyecto,
            "id_proyecto": id_proyecto,
            "id_version": id_version,
            "nombre_version": nombre_version,
            "id_version_insample": id_version_insample,
            "nombre_version_insample": nombre_version_insample
        }

        print("Datos enviados al servidor:", data)
        try:
            # Enviar datos como JSON en una solicitud POST
            starlette_response = requests.post(url, json=data, timeout=1)  # Tiempo de espera de 1 segundo
            if starlette_response.status_code == 200:
                print("Respuesta de la API de Starlette (in sample):", starlette_response.json())
                return starlette_response.json()  # Devuelve la respuesta JSON
            else:
                print("Error en la API de Starlette (in sample):", starlette_response.text)
                return {"error": starlette_response.text}
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud a la API de Starlette (in sample): {e}")
            return {"error": str(e)}
        



async def procesar_starlette_api_validacion_scoring(
    user_id, nombre_proyecto, id_proyecto, id_version, 
    nombre_version, id_version_insample, 
    nombre_version_insample, nombre_folder_validacion_scoring
):
    """Envía datos al API de Starlette para procesar 'validacion y scoring' de forma asincrónica."""
    
    url = "http://127.0.0.1:3000/api/process_user_id"  # Endpoint específico para in-sample
    data = {
        "user_id": user_id,
        "nombre_proyecto": nombre_proyecto,
        "id_proyecto": id_proyecto,
        "id_version": id_version,
        "nombre_version": nombre_version,
        "id_version_insample": id_version_insample,
        "nombre_version_insample": nombre_version_insample,
        "nombre_folder_validacion_scoring": nombre_folder_validacion_scoring
    }

    print("Datos enviados al servidor: validacion y scoring:", data)

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.post(url, json=data)
            
            if response.status_code == 200:
                print("Respuesta de la API de Starlette (validacion_scoring):", response.json())
                return response.json()  # Devuelve la respuesta JSON
            else:
                print("Error en la API de Starlette (validacion_scoring):", response.text)
                return {"error": response.text}
    
    except httpx.RequestError as e:
        print(f"Error en la solicitud a la API de Starlette (validacion_scoring): {e}")
        return {"error": str(e)}
    