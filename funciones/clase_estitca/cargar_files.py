from shiny import reactive, render, ui
from funciones.utils_2 import  get_datasets_directory, crear_carpeta_validacion_scoring, crear_carpeta_dataset
from api.db import *
from clases.global_session import *
from clases.global_sessionV2 import *
from clases.reactives_name import global_names_reactivos
from funciones.funciones_cargaDatos import guardar_archivo, verificar_archivo_sc, guardar_archivo_sc
from shiny.types import FileInfo
from global_names import global_name_out_of_Sample
from funciones_modelo.warning_model import check_if_exist_id_version_id_niveles_scord, create_modal_generic
from logica_users.utils.help_versios import obtener_opciones_versiones, obtener_ultimo_id_version
from clases.global_session import *
from datetime import datetime
import os
from api.db.up_date import *
from clases.global_sessionV3 import *
from funciones.cargar_archivosNEW import create_modal_warning_exist_file
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
            data_Set  = get_datasets_directory(
                global_session.get_id_user(), 
                global_session.get_id_proyecto(), 
                global_session.get_name_proyecto()
            )
            
            if global_session_V3.modelo_existe.get():
                ui.modal_show(create_modal_generic("cerrar_existe", f"Se le recuerda que usted en la versión {global_session.get_versiones_name()} tiene un modelo generado"))
             

            existe = verificar_archivo_sc(data_Set, input_name)
            if existe and self.select_overwrite.get() is False:
                print("pase el if?")
                ui.modal_show(create_modal_warning_exist_file(input_name, self.name_suffix, global_session.get_name_proyecto()))
                self.set_existe_file(True)
                return
                
            ruta_guardado = await guardar_archivo(input_file, self.name_suffix)
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")
            ##GUARDO LEL DATO CARGADO EN LA TABLA
            #insert_into_table("name_files", ['nombre_archivo', 'fecha_de_carga', 'project_id', 'version_id'], [input_name, fecha_de_carga, global_session.get_id_proyecto(), global_session.get_id_version()])
            print("pase antes de insertar??")
            insertar_nombre_file_desa_insa(
                db_path="Modeling_App.db",
                columns=['nombre_archivo', 'fecha_de_carga', 'project_id'],
                values=[input_name, fecha_de_carga, global_session.get_id_proyecto()]
            ) 
            
            global_names_reactivos.set_proceso_leer_dataset(True)
            
            print(f"id proyecto: {global_session.get_id_proyecto()}")
            
            files_name = get_records(
            table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            where_clause='project_id = ?',  # Cambiar la cláusula a usar project_id directamente
            where_params=(global_session.get_id_proyecto(),)
        )
            
            print(f"nombre files query: {files_name}")
            
            self.opciones_data.set(obtener_opciones_versiones(files_name, "id_files", "nombre_archivo"))
            
            self.dataSet_predeterminado_parms.set(obtener_ultimo_id_version(files_name, "id_files"))
            
            print(f"El archivo fue guardado en: {ruta_guardado}")
            
            print(self.opciones_data.get())
            print(self.dataSet_predeterminado_parms.get())
            print(files_name)
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
            
            validar_ids = check_if_exist_id_version_id_niveles_scord(global_session.get_id_version(), global_session.get_version_parametros_id())
            if validar_ids:
                ui.modal_show(create_modal_generic("boton_advertencia_files", f"Es obligatorio generar una versión de {global_name_out_of_Sample} y una versión para continuar."))
                return 
            validar_file = verificar_archivo_sc(data_Set, input_name)
            if validar_file and self.select_overwrite.get() is False:
                ui.modal_show(create_modal_warning_exist_file(input_name, self.name_suffix, global_session.get_name_proyecto()))
                self.set_existe_file(True)
                return
            
            file_name_without_extension = os.path.splitext(input_name)[0]
            print(f"Nombre del archivo recibido: {input_name}")

            # Guardar el archivo
            ruta_guardado = await guardar_archivo_sc(input_file, self.name_suffix)
            print(f"El archivo fue guardado en {ruta_guardado}")

            # Obtener fecha actual
            fecha_de_carga = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Insertar datos en la tabla
            id = insertar_nombre_file(input_name, global_session.get_id_proyecto())
            global_session_V2.set_id_Data_validacion_sc(id)
            # Extraer datos
            self.files_name.set(obtener_nombres_files_por_proyecto(global_session.get_id_proyecto()))

            # Actualizar opciones y seleccionar predeterminados
            global_session_V2.set_opciones_name_dataset_Validation_sc(obtener_opciones_versiones(self.files_name.get(), "id_nombre_file", "nombre_file"))
            
            self.data_predeterminado.set(obtener_ultimo_id_version(self.files_name.get(), 'id_nombre_file'))
            
            #opciones_actualizadas = [d["nombre_archivo_validation_sc"].rsplit('.', 1)[0] for d in files_name.get()]
            entrada, salida = crear_carpeta_validacion_scoring(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_id_version(), global_session.get_version_parametros_id(), global_session.get_versiones_parametros_nombre(), global_session.get_name_proyecto(), global_session.get_versiones_name(), file_name_without_extension)
            crear_carpeta_dataset(entrada)
            ui.update_select(
                "files_select_validation_scoring",
                choices=global_session_V2.get_opciones_name_dataset_Validation_sc(),
                selected=self.data_predeterminado.get()
            )

            self.select_overwrite.set(False)
        except Exception as e:
            # Manejar errores y notificar al usuario
            error_message = f"Error en loadOutSample: {e}"
            #ui.update_text("error_message", error_message)  # Asume que hay un output de texto para mostrar errores
            print(error_message)
    
     