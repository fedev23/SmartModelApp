import uuid
import datetime
import httpx
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse

# 🟡 Almacenamiento de sesiones (session_id -> datos)
session_store = {}

class SessionAPI(HTTPEndpoint):
    async def post(self, request):
        """Guarda la sesión de un usuario y devuelve session_id."""
        data = await request.json()
        user_id = data.get("user_id")
        is_logged_in = data.get("is_logged_in")

        if not user_id or is_logged_in is None:
            return JSONResponse({"error": "Faltan campos requeridos"}, status_code=400)

        # ✅ Genera session_id único
        session_id = str(uuid.uuid4())

        # ✅ Guarda la sesión usando session_id como clave
        session_store[session_id] = {
            "user_id": user_id,
            "is_logged_in": is_logged_in,
            "timestamp": datetime.datetime.now().isoformat()
        }

        return JSONResponse({
            "message": "Sesión guardada correctamente",
            "session_id": session_id
        }, status_code=200)

    async def get(self, request):
        """Obtiene la sesión usando session_id."""
        session_id = request.query_params.get("session_id")
        if not session_id:
            return JSONResponse({"error": "Se requiere 'session_id'"}, status_code=400)

        session = session_store.get(session_id)
        if session:
            return JSONResponse({
                "session_id": session_id,
                **session
            }, status_code=200)
        else:
            return JSONResponse({"error": "Sesión no encontrada"}, status_code=404)


    async def get_current_session(self):
        # Obtiene el session_id directamente desde session_store
        if session_store:
            for session_id, data in session_store.items():
                if data.get("is_logged_in"):
                    return session_id
        return None
    
    


async def consultar_session_api(session_id):
    """Consulta la API para obtener la sesión activa usando session_id."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"http://localhost:3000/api/session?session_id={session_id}",
                timeout=5
            )
            if response.status_code == 200:
                session_data = response.json()
                user_id = session_data.get("user_id")
                print(f"✅ Usuario activo: {user_id}")
                return user_id
            else:
                print(f"❌ Error al consultar sesión: {response.status_code} - {response.text}")
                return None
    except Exception as e:
        print(f"🚨 Error al conectar con la API de sesión: {e}")
        return None
