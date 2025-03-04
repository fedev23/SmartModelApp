import os
import tempfile
from shiny import ui, reactive, render
import requests
from urllib.parse import urlencode
from funciones.utils import create_zip_from_directory, create_zip_from_file_unico
import re
import requests
from auth.utils import help_api 
from urllib.parse import urlencode
from clases.global_session import global_session
from clases.global_sessionV2 import *


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
        self.path_resultados = ""
        self.proceso_ok = reactive.Value(False)
        self.proceso_user = reactive.Value(False)
        self.user = reactive.Value()
        self.path_salida =  reactive.Value()
        
    def obtener_user_id(self):
        @reactive.effect
        def enviar_session():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user_id_cleaned = user_id.replace('|', '_') 
                    self.proceso_user.set(True)
                    path_datos_salida  = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
                    self.path_salida.set(path_datos_salida)
                    self.user.set(user_id_cleaned)
                    return user_id_cleaned
    
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
            resultado_path = next((r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id), None)
            if self.proceso_user.get():
                if resultado_path and self.accordion_open[resultado_id].get():

                    try:
                        iframe_src = f"/api/user_files?{urlencode({'user_id': self.user.get(), 'nombre_proyecto': global_session.get_name_proyecto(), 'id_proyecto': global_session.get_id_proyecto(), 'id_version': global_session.get_id_version(), 'nombre_version': global_session.get_versiones_name(), 'file_name': os.path.basename(resultado_path)})}"
                        
                        # Verificar si el archivo existe en el sistema de archivos
                        file_path = f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{self.user.get()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/Reportes/{os.path.basename(resultado_path)}"
                        print(f"viendo file path, {file_path}")
                        if os.path.exists(file_path):
                            return ui.div(
                                ui.tags.iframe(src=iframe_src, width='350%', height='500px')
                            )
                        else:
                            print(f"El archivo no existe desa?: {file_path}")
                            return ui.div()
                            
                    except Exception as e:
                        print(f"Error: {e}")
                        return ui.div()
                else:
                    return ui.HTML("<p>Archivo no encontrado</p>") 
                 
    def html_output_in_sample(self, resultado_id):
         # Obtener el estado del acordeón específico para este resultado_id
        if resultado_id in self.accordion_open:
            resultado_path = next((r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id), None)
            if self.proceso_user.get():
                if resultado_path and self.accordion_open[resultado_id].get():

                    try:
                        iframe_src = f"/api/user_files?{urlencode({'user_id': self.user.get(), 'nombre_proyecto': global_session.get_name_proyecto(), 'id_proyecto': global_session.get_id_proyecto(), 'id_version': global_session.get_id_version(), 'nombre_version': global_session.get_versiones_name(), 'id_version_insample': global_session.get_version_parametros_id(), 'nombre_version_insample': global_session.get_versiones_parametros_nombre(), 'file_name': os.path.basename(resultado_path)})}"
                        salida =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/Reportes/{os.path.basename(resultado_path)}'
                    
                        if os.path.exists(salida):
                            return ui.div(
                                ui.tags.iframe(src=iframe_src, width='350%', height='500px')
                            )
                        else:
                            print(f"El archivo no existe in sample?: {salida}")
                            return ui.div()
                            
                    except Exception as e:
                        print(f"Error: {e}")
                        return ui.div()
                else:
                    return ui.HTML("<p>Archivo no encontrado</p>") 
                
                
    def html_output_validacion_scoring(self, resultado_id):
         # Obtener el estado del acordeón específico para este resultado_id
        if resultado_id in self.accordion_open:
            resultado_path = next((r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id), None)
            if self.proceso_user.get():
                if resultado_path and self.accordion_open[resultado_id].get():

                    try:
                        iframe_src = f"/api/user_files?{urlencode({'user_id': self.user.get(), 'nombre_proyecto': global_session.get_name_proyecto(), 'id_proyecto': global_session.get_id_proyecto(), 'id_version': global_session.get_id_version(), 'nombre_version': global_session.get_versiones_name(), 'id_version_insample': global_session.get_version_parametros_id(), 'nombre_version_insample': global_session.get_versiones_parametros_nombre(), 'nombre_folder_validacion_scoring': global_session_V2.nombre_file_sin_extension_validacion_scoring.get(),'file_name': os.path.basename(resultado_path)})}"
                        #C:\Users\fvillanueva\Desktop\SmartModel_new_version\new_version_new\Automat\datos_salida_auth0_670d225413861ad9fa6849d3\proyecto_67_ProyectoA\version_69_version22\version_parametros_65_version_prueba_de_22\set_Cliente_Conocido
                        salida =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/{global_session_V2.nombre_file_sin_extension_validacion_scoring.get()}/Reportes/{os.path.basename(resultado_path)}'

                        print(f"viendo salida: {salida}")
                        if os.path.exists(salida):
                            print(f"¿Existe la carpeta?: {os.path.isdir(os.path.dirname(salida))}")
                            print(f"¿Existe el archivo?: {os.path.isfile(salida)}")

                            return ui.div(
                                ui.tags.iframe(src=iframe_src, width='350%', height='500px')
                            )
                        else:
                            print(f"El archivo no existe en html_output_validacion_scoring: {salida}")
                            return ui.div()
                            
                    except Exception as e:
                        print(f"Error: {e}")
                        return ui.div()
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
            resultado_path = next(
                (r['resultado_path'] for r in self.resultados if r['resultado_id'] == resultado_id),
                None
            )
            if resultado_path and self.accordion_open[resultado_id].get():
                temp_zip_path = tempfile.NamedTemporaryFile(delete=False).name + '.zip'
                # Se construye la ruta completa uniendo self.path_resultados y resultado_id
                print(self.path_resultados, "viendo path resultados")
                full_path = os.path.join(self.path_resultados, resultado_path)
                print(f"viendo full path {full_path}")
                create_zip_from_file_unico(full_path, temp_zip_path)
                return temp_zip_path
            else:
                print("<p>Archivo no encontrado</p>")            