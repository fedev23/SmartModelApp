import pandas as pd
import os
from shiny import ui, reactive
from clases.global_name import global_name_manager

class CargarDatos:
    def __init__(self, file_info, delimitador, directorio_guardado):
        self.file_info = file_info
        self.delimitador = delimitador
        self.directorio_guardado = directorio_guardado
        self.name_file = reactive.Value(None)
        
    def procesar_delimitador(self):
        return self.delimitador.encode('utf-8').decode('unicode_escape')

    def cargar_datos(self):
        if not self.file_info:
            raise ValueError("No se seleccionó ningún archivo")
        
        file_path = self.file_info[0]["datapath"]
        file_name = self.file_info[0]["name"]
        if self.delimitador == '\\t':
            self.delimitador = '\t'
        print(self.delimitador, "paso por aca")
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path, sep=self.delimitador)
        elif file_name.endswith(".txt"):
            df = pd.read_table(file_path, sep=self.delimitador)
        else:
            raise ValueError("Tipo de archivo no soportado")

        nombre_archivo = os.path.basename(file_name)
        
        ruta_guardado = os.path.join(self.directorio_guardado, nombre_archivo)
        df.to_csv(ruta_guardado, index=False, sep=self.delimitador, quoting=0)
        self.name_file.set(nombre_archivo)
        
        return df, ruta_guardado, file_name

    
    def get_file_name_global(self):
        return self.name_file.get()
