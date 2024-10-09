import os
import tempfile
from shiny import ui, reactive
from funciones.utils import create_zip_from_directory, create_zip_from_file_unico
import re
#from IPython.display import display, HTML

def sanitize_id(id_string):
    # Reemplazar cualquier cosa que no sea letra, num o guion bajo con un guion bajo
        return re.sub(r'\W+', '_', id_string)

class ResultadoClass:
    def __init__(self, resultado_id, resultado_path, directory_path, salida, descarga_unic, salida_descarga_unic):
        self.resultado_id = str(resultado_id)
        self.descarga_unic = descarga_unic
        self.salida_descarga_unic = salida_descarga_unic
        self.salida = salida
        self.resultado_path = resultado_path
        self.directory_path = directory_path
        self.html_content = reactive.Value("")
        self.accordion_open = reactive.Value(False)
        


    def resultado_card(self):
        self.ver_resultado() 
        sanitize_id(self.resultado_id)
        print(self.resultado_id)
        #self.abrir_acordeon(input)
        return ui.card(
            ui.card_header(
                f"Resultado ({self.resultado_id})",
                ui.accordion(
                    ui.accordion_panel(
                        f"Resultado ({self.resultado_id})",
                        ui.div(
                            ui.div(
                              #self.html_output_prueba(), 
                               ui.output_ui(self.salida), 
                            ),
                            #ui.output_ui(self.salida),
                            ui.download_button(self.descarga_unic,  f"Descargar resultado {self.resultado_id}"),
                        ),
                        value=f"panel_{self.resultado_id}",
                        class_="d-flex justify-content-between align-items-center"
                    ),
                    id=f"accordion_{self.resultado_id}",
                    open=False
                ),
            )
        )

    def abrir_acordeon(self, input):
        @reactive.Effect
        @reactive.event(input[f"accordion_{self.resultado_id}"])
        def activar_boton():
            print("Acordeón abierto")
            self.accordion_open.set(True)
            self.ver_resultado()

    def ver_resultado(self):
        if os.path.exists(self.resultado_path):
            with open(self.resultado_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print("HTML cargado exitosamente.")
                self.html_content.set(content)
        else:
            print("Archivo no encontrado.")
            self.html_content.set("<p>Archivo no encontrado</p>")

    def html_output_prueba(self):
        print(f"Estado del acordeón: {self.accordion_open.get()}")
        if self.accordion_open.get():
            iframe_src = f'http://127.0.0.1:5000/static/{os.path.basename(self.resultado_path)}'
            return ui.div(
                ui.tags.iframe(src=iframe_src, width='350%', height='500px'))
        return ui.HTML("<p>Archivo no encontrado</p>")
    
    def boton_para_descagar_unico(self):
        print(f"Estado del acordeón en descarga unica: {self.accordion_open.get()}")
        if self.accordion_open.get():
            return ui.download_button(self.descarga_unic, "Descagar" )
    

    def descargar_resultados(self):
        temp_zip_path = tempfile.NamedTemporaryFile(delete=False).name + '.zip'
        create_zip_from_directory(self.directory_path, temp_zip_path)
        return temp_zip_path
    
    def descargar_unico_html(self):
        temp_zip_path = tempfile.NamedTemporaryFile(delete=False).name + '.zip'
        create_zip_from_file_unico(self.resultado_path, temp_zip_path)
        return temp_zip_path