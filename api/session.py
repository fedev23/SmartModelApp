import requests
from shiny import reactive


def check_user_authenticated():
    try:
        # Hacer una solicitud al servidor Flask para obtener la sesión
        response = requests.get("http://localhost:3000/get_session")
        print(response)
        session_data = response.json()
        if session_data["authenticated"]:
            # Guardar el ID del usuario en una variable reactiva en Shiny
            user_session.set({"user_id": session_data["user_id"], "authenticated": True})
        else:
            user_session.set({"user_id": None, "authenticated": False})
    except Exception as e:
        print(f"Error al verificar la sesión: {e}")

# Variable reactiva para almacenar el estado del usuario
user_session = reactive.Value({"user_id": None, "authenticated": False})