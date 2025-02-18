from shiny import reactive, render, ui, Inputs, Outputs, Session
from clases.global_session import *
def server_redireccionamiento(input: Inputs, output: Outputs, session: Session):
 
    @reactive.effect
    async def rederic():
        if session.request.path == "/shiny":
            session_id = global_session.session_state.get()
            if session_id["is_logged_in"]:
                await session.send_custom_message('navigate_uno', '/shiny')
            else:
                await session.send_custom_message('navigate_uno', '/login')
            