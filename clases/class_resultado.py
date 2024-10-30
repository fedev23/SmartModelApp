import os
import tempfile
from shiny import ui, reactive, render
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from funciones.utils import create_zip_from_directory, create_zip_from_file_unico
import re
from clases.global_session import global_session


#static_app = StaticFiles(directory='/mnt/c/Users/fvillanueva/flask_prueba/static', html=True)

def sanitize_id(id_string):
    # Reemplazar cualquier cosa que no sea letra, num o guion bajo con un guion bajo
    return re.sub(r'\W+', '_', id_string)

class ResultadoClassPrueba:
    def __init__(self, resultados):
        # resultados será una lista de diccionarios con resultado_id, resultado_path, directory_path, salida, descarga_unic, salida_descarga_unic
        self.resultados = resultados
        self.html_content = {r['resultado_id']: reactive.Value("") for r in resultados}
        self.accordion_open = {r['resultado_id']: reactive.Value(False) for r in resultados}
        self.proceso_ok = reactive.Value(False)
        
    def obtener_user_id(self):
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user_id_cleaned = user_id.replace('|', '_')
                    print(user_id_cleaned)
    
    def resultado_cards(self):
        # Crear todas las tarjetas de resultados
        cards = []
        for r in self.resultados:
            cards.append(self.create_resultado_card(r))
        return ui.div(*cards)

    def create_resultado_card(self, r):
        sanitized_id = sanitize_id(r['resultado_id'])
        return ui.card(
            ui.card_header(
                ui.accordion(
                    ui.accordion_panel(
                        f"Resultado ({r['resultado_id']})",
                        ui.div(
                            ui.div(ui.output_ui(r['salida'])),
                            ui.div(ui.output_ui(r['salida_unic'])),
                            ui.download_button(f"{r['descarga_unic']}",  f"Descargar resultado {r['resultado_id']}"),
                            #self.make_example(r['resultado_id'], 'Descargar resultado', 'Título del ejemplo')
                        ),
                        value=f"panel_{r['resultado_id']}",
                        class_="d-flex justify-content-between align-items-center"
                    ),
                    id=f"accordion_{r['resultado_id']}",
                    open=False
                ),
            )
        )

    def abrir_acordeon(self, input):
        for r in self.resultados:
            # Usa functools.partial para pasar el resultado_id correcto
            @reactive.Effect
            @reactive.event(input[f"accordion_{r['resultado_id']}"])
            def activar_boton(id=r['resultado_id']):
                #print(f"Estado del acordeón: {self.accordion_open[id].get()}")
                self.accordion_open[id].set(True)
                self.html_output_prueba(id)
                self.descargar_unico_html(id)
                self.boton_para_descagar_unico(id)
                self.proceso_ok.set(True)

    def html_output_prueba(self, resultado_id):
        # Obtener el estado del acordeón específico para este resultado_id
        if resultado_id in self.accordion_open:
            #print(f"resultado esperado", resultado_id)
            
            resultado_path = next((r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id), None)
            print(resultado_path)
            if resultado_path and self.accordion_open[resultado_id].get():
                user_id = self.obtener_user_id()
                iframe_src = f'/static/{os.path.basename(resultado_path)}?user_id={user_id}'
                return ui.div(
                    ui.tags.iframe(src=iframe_src, width='350%', height='500px'))
            else:
                return ui.HTML("<p>Archivo no encontrado</p>")
       

    def descargar_resultados(self, directory_path):
        temp_zip_path = tempfile.NamedTemporaryFile(delete=False).name + '.zip'
        create_zip_from_directory(directory_path, temp_zip_path)
        return temp_zip_path
    
    def boton_para_descagar_unico(self, resultado_id):
        if self.proceso_ok.get():
            return ui.download_button(resultado_id, f"Descargar resultado {resultado_id}")

    def descargar_unico_html(self, resultado_id):
        if resultado_id in self.accordion_open:
                #print(f"resultado esperado", resultado_id)
                resultado_path = next((r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id), None)
                #print(f"Resultado path: {resultado_path}")
                if resultado_path and self.accordion_open[resultado_id].get():
                    temp_zip_path = tempfile.NamedTemporaryFile(delete=False).name + '.zip'
                    #print(f"Archivo ZIP temporal: {temp_zip_path}")
                    create_zip_from_file_unico(resultado_path, temp_zip_path)
                    return temp_zip_path
                else:
                    print("<p>Archivo no encontrado</p>")
                