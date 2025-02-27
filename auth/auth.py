from shiny import reactive, render, ui, Inputs, Outputs, Session
import requests
from funciones.utils_2 import  mostrar_error
from funciones.utils_2 import crear_carpetas_por_id_user
from clases.global_session import global_session
from logica_users.help_user_insert.table_user import *
from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse, RedirectResponse
import requests
import sys, asyncio
import httpx
import redis.asyncio as redis



configuration = {
    "Security": {
        "Auth0": {
            "ClientId": "jR4Rqx9qc86wY0oCkqJXy5x8Ph6KxmuU",
            "ClientSecret": "KDF6Wqu638CPm630aF-aa1g1jGTqR1SZehllkypMBhZhyfOYMuLifAhW1WwxD_S1",
            "Domain": "dev-qpjdn3ayg3o85irl.us.auth0.com"
        }
    }
}

async def obtener_token(username, password, configuration):
    """Obtiene el token desde Auth0 (async) usando httpx."""
    data = {
        "client_id": configuration["Security"]["Auth0"]["ClientId"],
        "client_secret": configuration["Security"]["Auth0"]["ClientSecret"],
        "grant_type": "password",
        "username": username,
        "password": password,
        "audience": "https://beApp.com/",
        "scope": "openid profile read:users"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://{configuration['Security']['Auth0']['Domain']}/oauth/token",
                data=data,
                timeout=5
            )
            if response.status_code == 200:
                return response.json().get("access_token")
            else:
                print(f"❌ Error en la autenticación: {response.text}")
                return None
    except httpx.RequestError as e:
        print(f"🚨 Error de conexión a Auth0: {e}")
        return None
    
            
async def obtener_user_info(access_token, configuration):
    """Obtiene el perfil del usuario desde Auth0 usando el token (async)."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://{configuration['Security']['Auth0']['Domain']}/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if response.status_code == 200:
                return response.json()  # ✅ Devuelve el perfil completo
            else:
                print("❌ Error al obtener información del usuario:", response.text)
                return None
    except httpx.RequestError as e:
        print(f"🚨 Error de conexión a Auth0: {e}")
        return None
    
    
    
async def login_async(payload):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:3000/api/auth/login",
                json=payload,
                timeout=5,
                follow_redirects=False
            )
            print(f"Status: {response.status_code}")
            print(f"Headers: {response.headers}")
            print(f"Body: {response.text}")
            return response
    except httpx.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return None


redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def server_login(input: Inputs, output: Outputs, session: Session):
    count = reactive.Value(0)
    mensaje = reactive.Value(None)
    proceso = reactive.Value(False)
    
    

    async def enviar_session_api(user_id, is_logged_in):
        """Envía el estado de sesión a la API y obtiene session_id."""
        payload = {
            "user_id": user_id,
            "is_logged_in": is_logged_in
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "http://localhost:3000/api/session",
                    json=payload,
                    timeout=5
                )
                if response.status_code == 200:
                    session_id = response.json().get("session_id")
                    print(f"📤 Sesión guardada. session_id: {session_id}")
                    return session_id
                else:
                    print(f"❌ Error al guardar sesión: {response.status_code}")
                    return None
        except Exception as e:
            print(f"🚨 Error de conexión: {e}")
            return None
        

    async def manejar_login_async(payload):
        access_token = await obtener_token(payload["username"], payload["password"], configuration)
        if not access_token:
            mensaje.set("Contraseña o usuario incorrecto.")
            proceso.set(True)
            return

        user_info = await obtener_user_info(access_token, configuration)
        if user_info and "sub" in user_info:
            user_id = user_info["sub"].replace("|", "_")
            print(f"✅ Usuario autenticado: {user_id}")

            # 1) Guarda sesión local (Shiny):
            global_session.session_state.set({
                "is_logged_in": True,
                "id": user_id
            })

            #await redis_client.setex(user_id, 7200, user_id)
            #await session.send_custom_message("reset_ui", {})
            
            async with httpx.AsyncClient() as client:
                r = await client.post("http://localhost:3000/api/login_starlette_session", json={"user_id": user_id})
                # Este endpoint, al recibir la request, hará: request.session["user_id"] = user_id
                # Y Starlette enviará la cookie de sesión al navegador.

            # 3) Redirige a /shiny/ (puedes seguir enviando el token si quieres),
            # pero si ya estás en la misma sesión, no lo necesitas en cada request.
                await session.send_custom_message('crearCookie', {"user_id": user_id})

        else:
            mensaje.set("No se pudo obtener la información del usuario.")
    
            
    
    @reactive.effect
    @reactive.event(input.login_button)
    def manejar_login():
        """Inicia el proceso de login al presionar el botón."""
        payload = {"username": input.username(), "password": input.password()}
        print("Iniciando login...", flush=True)
        
        # ✅ Usar asyncio.create_task() para no bloquear el loop
        asyncio.ensure_future(manejar_login_async(payload))    
        
        if mensaje.get() is not None:
            proceso.set(True)

        
         
    @output
    @render.text   
    def login_message():
        if proceso.get():
            return mostrar_error(mensaje.get())
        
        
        
