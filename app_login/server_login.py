from shiny import ui, render, reactive, App
from app_login.app_ui import ui_login
from auth.auth import server_login

def create_login(input, output, session):
    server_login(input, output, session)
    


login_ui = App(ui_login, create_login)

    