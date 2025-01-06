from shiny import reactive, render, ui
from funciones.create_param import create_screen
from clases.global_modelo import global_desarollo
from clases.class_screens import ScreenClass
from funciones.utils import retornar_card
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils_2 import get_datasets_directory_data_set_versiones, render_data_summary, aplicar_transformaciones, mostrar_error, cambiarAstring, trans_nulos_adic, get_datasets_directory, detectar_delimitador
from api.db import *
from clases.global_session import *
from clases.global_sessionV2 import *
from clases.reactives_name import global_names_reactivos
from funciones.funciones_cargaDatos import guardar_archivo, verificar_archivo, verificar_archivo_sc, guardar_archivo_sc
from shiny.types import FileInfo
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version
from clases.global_session import *
from datetime import datetime
from funciones.cargar_archivosNEW import create_modal_warning_exist_file, create_modal_warning_exist_file_for_full_or_sc
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
        self.files_name = reactive.value()
        self.data_predeterminado = reactive.Value()
        
        
    
    
    async def cargar_Datos_desarrollo(self,input_file):
        try:
            file: list[FileInfo] | None = input_file()
            input_name = file[0]['name']
            global_names_reactivos.set_name_data_Set(input_name)
            

            existe = verificar_archivo()
            print(existe, "que valor me da?")
            if existe and self.select_overwrite.get() is False:
                print("pase el if?")
                ui.modal_show(create_modal_warning_exist_file(input_name, self.name_suffix, global_session.get_versiones_name()))
                self.set_existe_file(True)
                return
                
            ruta_guardado = await guardar_archivo(input_file, self.name_suffix)
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")
            ##GUARDO LEL DATO CARGADO EN LA TABLA
            #insert_into_table("name_files", ['nombre_archivo', 'fecha_de_carga', 'project_id', 'version_id'], [input_name, fecha_de_carga, global_session.get_id_proyecto(), global_session.get_id_version()])
            print("pase antes de insertar??")
            insert_into_table(
                table_name="name_files",
                columns=['nombre_archivo', 'fecha_de_carga', 'version_id'],
                values=[input_name, fecha_de_carga, global_session.get_id_version()]
            ) 
            
            global_names_reactivos.set_proceso_leer_dataset(True)
            
            files_name = get_records(
            table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
            where_clause='version.version_id = ?',
            where_params=(global_session.get_id_version(),)
        )
            
         
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
        
        
    
    async def cargar_datos_validacion_scroing(self, input_file):
        try:
            file: list[FileInfo] | None = input_file()
            input_name = file[0]['name']
            if not file:
                raise ValueError("No se recibió ningún archivo para validar.")

            data_Set  = get_datasets_directory(
                global_session.get_id_user(), 
                global_session.get_id_proyecto(), 
                global_session.get_name_proyecto()
            )
            validar_file = verificar_archivo_sc(data_Set, input_name)
            if validar_file and self.select_overwrite.get() is False:
                ui.modal_show(create_modal_warning_exist_file(input_name, self.name_suffix, global_session.get_versiones_name()))
                self.set_existe_file(True)
                return
            
            print(f"Nombre del archivo recibido: {input_name}")

            # Guardar el archivo
            ruta_guardado = await guardar_archivo_sc(input_file, self.name_suffix)
            print(f"El archivo fue guardado en {ruta_guardado}")

            # Obtener fecha actual
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Insertar datos en la tabla
            id = insert_into_table(
                table_name="validation_scoring",
                columns=['nombre_archivo_validation_sc', 'fecha_de_carga', 'version_id'],
                values=[input_name, fecha_de_carga, global_session.get_id_version()]
            )
            
            print("Datos insertados en la tabla validation_scoring.")
            global_session_V2.set_id_Data_validacion_sc(id)
            # Extraer datos
            self.files_name.set(get_records(
            table='validation_scoring',
            columns=['id_validacion_sc', 
                    'nombre_archivo_validation_sc', 
                    'fecha_de_carga'],
            join_clause='INNER JOIN version ON validation_scoring.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),)
        ))
            # Actualizar opciones y seleccionar predeterminados
            global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(self.files_name.get(), "id_validacion_sc", "nombre_archivo_validation_sc"))
            
            self.data_predeterminado.set(obtener_ultimo_id_version(self.files_name.get(), 'id_validacion_sc'))
            
            #opciones_actualizadas = [d["nombre_archivo_validation_sc"].rsplit('.', 1)[0] for d in files_name.get()]
            ui.update_select(
                "files_select_validation_scoring",
                choices=global_session_V2.get_opciones_name_dataset_Validation_sc(),
                selected=self.data_predeterminado.get()
            )
            print("Opciones y selección actualizadas correctamente.")
            self.select_overwrite.set(False)
        except Exception as e:
            # Manejar errores y notificar al usuario
            error_message = f"Error en loadOutSample: {e}"
            #ui.update_text("error_message", error_message)  # Asume que hay un output de texto para mostrar errores
            print(error_message)
    
     