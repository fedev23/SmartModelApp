from shiny import ui, reactive, Session, Outputs, Inputs




from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware


async def logout_starlette_session(request):
    # Limpiar la sesión del lado del servidor
    request.session.clear()
    # Preparar la respuesta
    response = JSONResponse({"message": "Sesión cerrada"})
    # Eliminar la cookie de sesión (asegúrate de que "session" sea el nombre correcto)
    response.delete_cookie("session")
    return response


def server_log_out(input: Inputs, output: Outputs, session: Session):
     
    @reactive.effect
    @reactive.event(input.cerrar_session)
    async def log_out():
        await session.send_custom_message("logout", {"redirect_url": "http://localhost:3000/login"})
        await session.close()
        