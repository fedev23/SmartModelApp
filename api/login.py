# api/login_endpoint.py
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import RedirectResponse

from auth.auth import obtener_token, obtener_user_info , configuration #  lógica de Auth0


class LoginPageEndpoint(HTTPEndpoint):
    async def get(self, request: Request):
        # Limpia la sesión para forzar un nuevo login
        request.session.clear()
        
        response = RedirectResponse(url="/login")
        # Eliminar la cookie de sesión
        response.delete_cookie("session")
        
        return response
    

class LoginEndpoint(HTTPEndpoint):
    async def post(self, request: Request):
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        # 1) Obtener token de Auth0
        access_token = await obtener_token(username, password, configuration)
        if not access_token:
            return JSONResponse({"error": "No se recibió el token de acceso."}, status_code=401)

        # 2) Obtener user_info
        user_info = await obtener_user_info(access_token, configuration)
        if not user_info or "sub" not in user_info:
            return JSONResponse({"error": "No se pudo obtener la información del usuario."}, status_code=401)
        
        # 3) Tomar user_id y guardarlo en la sesión
        user_id = user_info["sub"].replace("|", "_")
        request.session["user_id"] = user_id
        print(f"✅ Usuario autenticado: {user_id}")

        return JSONResponse({"message": "Login exitoso", "user_id": user_id}, status_code=200)


class LoginStarletteSessionEndpoint(HTTPEndpoint):
    async def post(self, request: Request):
        
        request.session.clear()
        data = await request.json()
        user_id = data.get("user_id")
        if not user_id:
            return JSONResponse({"error": "Falta user_id"}, status_code=400)

        # Guarda el user_id en la sesión de Starlette
        request.session["user_id"] = user_id
        print(f"✅ user_id {user_id} guardado en session Starlette")

        return JSONResponse({"message": "Starlette session updated."}, status_code=200)