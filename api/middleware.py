# api/middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import HTMLResponse
import logging
from starlette.responses import JSONResponse
from starlette.background import BackgroundTask


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Permitir sin autenticación y limpiar sesión en rutas de login
        if (
            path.startswith("/login") or
            path.startswith("/api/login") or
            path.startswith("/api/session") or
            path.startswith("/api/validate_token") or
            path.startswith("/api/logout_starlette_session") or
            path.startswith("/api/process_user_id")
        ):
            # Si está en /login o /api/login, limpiar toda la sesión
            if path.startswith("/login") or path.startswith("/api/login_endpoint"):
                if "user_id" in request.session:
                    logger.info(f"Limpiando sesión completa para la ruta {path}")
                    request.session.clear()  # Elimina todos los datos de la sesión
            return await call_next(request)

        if path.startswith("/shiny/session/") and "/download/" in path:
            logger.info("Ruta de descarga de Shiny, pasando sin autenticación")
            return await call_next(request)
        
        # Verificar si hay user_id
        user_id = request.session.get("user_id")
        
        print(user_id,"viendo user id!")
        if not user_id:
            return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Unauthorized - 401</title>
            <script src="https://cdn.tailwindcss.com"></script>
        </head>
        <body class="min-h-screen bg-gray-50 flex items-center justify-center p-4">
            <main class="max-w-lg mx-auto text-center">
                <div class="space-y-8">
                    <!-- Error Code -->
                    <h1 class="text-9xl font-extrabold text-gray-800">401</h1>

                    <!-- Error Message -->
                    <div class="space-y-4">
                        <h2 class="text-3xl font-semibold text-gray-700">Unauthorized</h2>
                        <p class="text-gray-600">You must be logged in to access this page.</p>
                    </div>

                    <!-- Back to Login Button -->
                    <div>
                        <a href="/login" class="inline-flex items-center justify-center px-6 py-3 text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 rounded-lg transition-colors duration-200">
                            Go to Login
                        </a>
                    </div>

                    <!-- Auto Redirect in 3 seconds -->
                    <script>
                        setTimeout(function() {
                            window.location.href = "/login";
                        }, 3000);
                    </script>

                </div>
            </main>
        </body>
        </html>
        """,
        status_code=401  # Código correcto para no autenticado
    )
        # Si existe user_id, deja pasar
        logger.info(f"Usuario autenticado {user_id}, accediendo a {path}")
        return await call_next(request)
    




