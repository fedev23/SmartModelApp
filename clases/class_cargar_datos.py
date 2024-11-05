import pandas as pd
import os
from shiny import ui, reactive
from clases.global_reactives import global_estados
import csv

class CargarDatos:
    def __init__(self, file_info, directorio_guardado):
        self.file_info = file_info
        self.directorio_guardado = directorio_guardado
        self.name_file = reactive.Value(None)
        
    def detectar_delimitador(self , file_path):
        """Detecta el delimitador de un archivo de texto o CSV automáticamente."""
        with open(file_path, 'r') as file:
            dialect = csv.Sniffer().sniff(file.readline(), delimiters=";,|\t")
            print(dialect.delimiter)
            return dialect.delimiter
            

    def cargar_datos(self):
        if not self.file_info:
            raise ValueError("No se seleccionó ningún archivo")
        
        file_path = self.file_info[0]["datapath"]
        file_name = self.file_info[0]["name"]
        delimitador_detectado = self.detectar_delimitador(file_path)
        global_estados.set_delimitador(delimitador_detectado)
        
        
        if file_name.endswith(".csv"):
            df = pd.read_csv(file_path, sep=delimitador_detectado)
        elif file_name.endswith(".txt"):
            df = pd.read_table(file_path, sep=delimitador_detectado)
        else:
            raise ValueError("Tipo de archivo no soportado")

        nombre_archivo = os.path.basename(file_name)
        
        ruta_guardado = os.path.join(self.directorio_guardado, nombre_archivo)
        df.to_csv(ruta_guardado, index=False, sep=delimitador_detectado, quoting=0)
        self.name_file.set(nombre_archivo)
        
        return df, ruta_guardado, file_name

    
    def get_file_name_global(self):
        return self.name_file.get()
