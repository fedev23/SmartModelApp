import pandas as pd
import os
import csv
from funciones.utils_2 import detectar_delimitador, get_datasets_directory
from clases.global_reactives import global_estados

class DatasetHandler:
    @staticmethod
    def leer_dataset(user_id, proyecto_id, name_proyect, dataset_name):
        """
        Lee un dataset basado en el usuario, proyecto y nombre del dataset.

        Args:
            user_id (str): ID del usuario.
            proyecto_id (str): ID del proyecto.
            name_proyect (str): Nombre del proyecto.
            dataset_name (str): Nombre del archivo del dataset.

        Returns:
            pd.DataFrame: Las primeras 10 filas del dataset si se encuentra, o un DataFrame vacío.
        """
        # Obtener la ruta de la carpeta de datasets
        datasets_directory = get_datasets_directory(user_id, proyecto_id, name_proyect)
        
        # Verificar que la carpeta de datasets no sea None
        if datasets_directory is None:
            print("No se encontró la carpeta de datasets.")
            return pd.DataFrame()  # Retornar un DataFrame vacío
        
        # Construir la ruta completa del archivo del dataset
        dataset_path = os.path.join(datasets_directory, dataset_name)
        
        # Verificar que el archivo existe
        if not os.path.exists(dataset_path):
            print(f"El archivo {dataset_path} no existe.")
            return pd.DataFrame()  # Retornar un DataFrame vacío
            
        # Leer el archivo de datos usando pandas
        try:
            # Detectar el delimitador del archivo
            delimitador = detectar_delimitador(dataset_path)
            global_estados.set_delimitador(delimitador)
            
            # Leer el archivo con el delimitador detectado
            dataset = pd.read_csv(dataset_path, delimiter=delimitador)
            print(f"Dataset {dataset_name} leído correctamente.")
            
            # Retornar las primeras 10 filas del dataset
            return dataset.head(10)

        except Exception as e:
            print(f"Error al leer el dataset: {e}")
            return pd.DataFrame()


