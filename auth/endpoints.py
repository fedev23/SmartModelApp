
from auth.auth import obtener_token, configuration
from starlette.responses import RedirectResponse, JSONResponse
from starlette.endpoints import HTTPEndpoint

class Auth0LoginEndpoint(HTTPEndpoint):
    async def post(self, request):
        data = await request.json()
        print(f"viendo data {data}")
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            return JSONResponse({"error": "Faltan credenciales (username o password)"}, status_code=400)
        
        # Llamada a la API de Auth0 para obtener el token
        access_token = obtener_token(username, password, configuration)
        
        if access_token:
            # Si la autenticación es exitosa, puedes realizar acciones adicionales:
            # - Obtener información del usuario, guardar en la sesión, etc.
            # Aquí, por simplicidad, redirigimos a la pantalla de dashboard (o a otra ruta deseada)
            return RedirectResponse(url="/shiny/", status_code=302)
        else:
            # En caso de error, se informa al usuario
            return JSONResponse({"error": "Autenticación fallida. Verifica tus credenciales."}, status_code=401)        
