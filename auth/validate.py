# api/endpoints_auth.py
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
import httpx
import os
from dotenv import load_dotenv


AUTH0_DOMAIN = "dev-qpjdn3ayg3o85irl.us.auth0.com"



class ValidateTokenEndpoint(HTTPEndpoint):
    async def post(self, request):
        print("🔍 Iniciando validación de token...")
        data = await request.json()
        token = data.get("access_token")
        print(f"🔑 Token recibido: {token}")

        if not token:
            print("❌ Token no proporcionado")
            return JSONResponse({"error": "Token no proporcionado"}, status_code=401)

        try:
            async with httpx.AsyncClient() as client:
                print("🔄 Enviando solicitud a Auth0 para validación...")
                response = await client.get(
                    f"https://{AUTH0_DOMAIN}/userinfo",
                    headers={"Authorization": f"Bearer {token}"}
                )
                print(f"📥 Respuesta de Auth0: {response.status_code}, {response.text}")
                if response.status_code == 200:
                    print("✅ Token válido. Redirigiendo a /shiny")
                    return JSONResponse({"redirect_url": "http://localhost:3000/shiny/"}, status_code=200)

                else:
                    print("❌ Token inválido")
                    return JSONResponse({"error": "Token inválido"}, status_code=401)
        except Exception as e:
            print(f"🚨 Error interno: {str(e)}")
            return JSONResponse({"error": f"Error interno: {str(e)}"}, status_code=500)
