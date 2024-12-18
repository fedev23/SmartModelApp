from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_modelo import global_desarollo
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import get_user_directory, render_data_summary, aplicar_transformaciones, mostrar_error, cambiarAstring, trans_nulos_adic, get_datasets_directory, detectar_delimitador
from api.db import *
from clases.global_session import *
from clases.global_sessionV2 import *
from clases.reactives_name import global_names_reactivos
from funciones.funciones_cargaDatos import guardar_archivo
from shiny.types import FileInfo
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version
from clases.global_session import *
from clases.class_validacion import Validator
from clases.loadJson import LoadJson
from datetime import datetime
from clases.global_reactives import global_estados
from funciones.cargar_archivosNEW import mover_y_renombrar_archivo, verificar_archivo, create_modal_warning_exist_file
import os 
from clases.reactives_name import global_names_reactivos


class FilesLoad:
    def __init__(self, name_suffix: str):
        """
        Constructor de la clase DatasetHandler.

        Args:
            name_suffix (str): Sufijo que se utilizará al guardar archivos.
        """
        self.name_suffix = name_suffix  # Atributo requerido
        self.opciones_data = reactive.Value()
        self.dataSet_predeterminado_parms = reactive.Value()
        self.existe_file = reactive.Value(False)
        self.select_overwrite = reactive.Value(False)
        
    
    
    async def cargar_Datos_desarrollo(self,input_file):
        try:
            file: list[FileInfo] | None = input_file()
            input_name = file[0]['name']
            global_names_reactivos.set_name_data_Set(input_name)
            
            existe = verificar_archivo(global_session.get_path_guardar_dataSet_en_proyectos(), input_name)
            print(f"estoy en existe {existe}")
            if existe and self.select_overwrite.get() is False:
              ui.modal_show(create_modal_warning_exist_file(input_name))
              self.set_existe_file(True)
              return
              
            ruta_guardado = await guardar_archivo(input_file, self.name_suffix)
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")
            ##GUARDO LEL DATO CARGADO EN LA TABLA
            #insert_into_table("name_files", ['nombre_archivo', 'fecha_de_carga', 'project_id', 'version_id'], [input_name, fecha_de_carga, global_session.get_id_proyecto(), global_session.get_id_version()])
            
            insert_record(
                database_path="Modeling_App.db",
                table="name_files",
                columns=['nombre_archivo', 'fecha_de_carga', 'version_id'],
                values=[input_name, fecha_de_carga, global_session.get_id_version()]
            ) 
            
            global_names_reactivos.set_proceso_leer_dataset(True)
            
            files_name = get_records(
            table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),))
            
         
            #print(files_name, "que tiene file name??")
            self.opciones_data.set(obtener_opciones_versiones(files_name, "id_files", "nombre_archivo"))
            
            self.dataSet_predeterminado_parms.set(obtener_ultimo_id_version(files_name, "id_files"))
            
            print(f"El archivo fue guardado en: {ruta_guardado}")
            ui.update_select("files_select", choices=self.opciones_data.get(), selected=self.dataSet_predeterminado_parms.get())
            self.select_overwrite.set(False)
            
        except Exception as e:
            print(f"Error en la carga de datos: {e}")
            
    
    
    def get_existe_file(self):
        return self.existe_file.get()
    
    
    def set_existe_file(self, boolean):
        self.existe_file.set(boolean)