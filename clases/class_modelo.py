
from shiny import reactive, render, ui
from clases.global_session import *
from datetime import datetime
import asyncio
import traceback
from funciones_modelo.warning_model import *
from api.db import *
import re
import asyncio
import re
import traceback
import os
from clases.global_sessionV3 import *
from funciones_modelo.global_estados_model import global_session_modelos
from clases.global_sessionV2 import *



class ModeloProceso:
    def __init__(self, nombre, directorio, script_name, script_path, name_file, mensaje_id, hora, estado, porcentaje_path):
        self.nombre = nombre
        self.name_file = name_file
        self.mensaje_id = mensaje_id
        self.directorio = directorio
        self.hora = hora
        self.estado = estado
        self.porcentaje_path = porcentaje_path
        self.script_name = script_name
        self.script_path = script_path
        self.proceso = reactive.Value(False)
        self.mensaje = reactive.Value("")
        self.click_counter = reactive.Value(0)  # Instancia de CargarDatos
        self.fecha_hora = reactive.Value("")
        self.extrat_hora = reactive.Value("")
        self.proceso_ok = reactive.Value(False)
        self.proceso_fallo = reactive.value(False)
        self.mensaje_error = reactive.Value("")
        self.pisar_el_modelo_actual = reactive.Value(False)
        self.porcentaje = reactive.value(0)
        self.file_reactivo = reactive.Value("")
        self.proceso_inicio = reactive.Value(False)
        
        

    async def run_script_prueba(self, progress_callback=None):
        # Convertir la ruta de Windows a WSL
        wsl_directorio = self.directorio
        comando = f'cd {wsl_directorio} && {self.script_path}'
        print(f"Comando a ejecutar: {comando}")

        try:
            # Verificar si `self.progress_file` está definido, de lo contrario usar uno por defecto

            # Crear el proceso de forma asíncrona
            process = await asyncio.create_subprocess_shell(
                comando,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Capturar la salida y los errores en tiempo real
            stdout, stderr = [], []
            progress_percentage = 0
            last_match = None  # Almacena el último valor de progreso válido

            self.porcentaje_path = os.path.join(self.porcentaje_path, "progreso.txt")
            # Eliminar el archivo de progreso si existe
            if os.path.exists(self.porcentaje_path):
                os.remove(self.porcentaje_path)

            async def write_progress_to_file(percentage):
                """Escribe el progreso en un archivo de texto"""
                try:
                    with open(self.porcentaje_path, "w") as file:
                        file.write(f"{percentage}%\n")
                except Exception as e:
                    print(f"Error escribiendo progreso en archivo: {str(e)}")

            async def read_stream(stream, output_list, output_prefix):
                nonlocal progress_percentage, last_match
                total_steps = None
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    decoded_line = line.decode('utf-8').strip()
                    output_list.append(decoded_line)
                    print(f"{output_prefix}: {decoded_line}")

                    # Intentar calcular el porcentaje si hay un patrón
                    match = re.search(r'(\d+)/(\d+)', decoded_line)
                    if match:
                        current_step = int(match.group(1))
                        total_steps = int(match.group(2))
                        last_match = (current_step, total_steps)  # Guardar el último match válido
                    
                    # Si hay un último match, calcular el progreso
                    if last_match:
                        progress_percentage = int((last_match[0] / last_match[1]) * 100)
                        self.porcentaje.set(progress_percentage)
                        print(f"Progreso: {progress_percentage}%")

                        # Guardar progreso en el archivo
                        await write_progress_to_file(progress_percentage)

                        # Usar callback para comunicar el progreso
                        if progress_callback:
                            progress_callback(progress_percentage)

            await asyncio.gather(
                read_stream(process.stdout, stdout, "STDOUT"),
                read_stream(process.stderr, stderr, "STDERR")
            )

            # Esperar a que el proceso termine
            return_code = await process.wait()

            # Unir todas las líneas capturadas en un solo string
            stdout_output = '\n'.join(stdout)
            stderr_output = '\n'.join(stderr)

            # Preparar el mensaje de error si hay un código de retorno diferente de 0
            error_message = f"Error durante la ejecución: {stderr_output}" if return_code != 0 else None

            return stdout_output, stderr_output, return_code, error_message, progress_percentage

        except Exception as e:
            # Capturar cualquier excepción y devolver el mensaje de error
            error_message = f"Excepción durante la ejecución: {str(e)}"
            print("Stacktrace:")
            traceback.print_exc()
            return None, None, 1, error_message, 0
    
    async def ejecutar_proceso_prueba(self, click_count, mensaje, proceso, porcentaje):
        try:
            
           
            def actualizar_progreso(porcentaje):
                self.porcentaje.set(porcentaje)
                self.proceso_inicio.set(True)
                print(f"Progreso actualizado: {porcentaje}%")  

            # Indicador de proceso en ejecución
            with ui.busy_indicators.use(spinners=True):
                # Ejecutar el script de manera asíncrona
                stdout, stderr, returncode, error_message, progress_percentage  = await self.run_script_prueba(progress_callback=actualizar_progreso)

                # Verificar el resultado y actualizar los valores reactivos
                if returncode != 0:
                    self.mensaje.set(error_message)
                    self.set_proceso(False)
                    self.proceso_fallo.set(True)
                else:
                   
                    self.mensaje.set("Ejecución completada con éxito.")
                    self.proceso_ok.set(True)
                    self.set_proceso(True)
                    

        except Exception as e:
            # Capturar cualquier excepción y actualizar el mensaje
            self.mensaje.set(f"Error inesperado: {str(e)}")
            print("Stacktrace:")
            traceback.print_exc()
    

    def set_proceso(self, proceso):
        self.proceso.set(proceso)
        
        
    def get_proceso(self):
        return self.proceso.get()

    def mostrar_mensaje(self):
        # if self.proceso.get():
        return self.mensaje.get()


    def log_fecha_hora(self):
        # Registra la fecha y hora actual
        now = datetime.datetime.now()
        # Formatear la fecha y hora para eliminar los milisegundos y microsegundos
        formatted_now = now.strftime('%Y-%m-%d %H:%M')
        self.fecha_hora = formatted_now
        return formatted_now

    def render_card(self, file_name, fecha, estado): 
        default_message = "Aún no se ha ejecutado el proceso."
        if self.mensaje_error:
            self.mensaje = self.mensaje_error
        if file_name is not None:
            if not fecha :
                fecha = "Fecha no disponible."
            if not estado:
               estado = "Estado no disponible."
            #fecha = self.log_fecha_hora()
            return ui.card(
                ui.card_header(
                    "",
                    #ui.p(f"Nombre del archivo: {file_name}", style="margin: 0; line-height: 1.5; vertical-align: middle;"), 
                    #ui.p(f"Fecha de última ejecución: {str(fecha_hora)}"),
                    ui.p(f"Estado de la ultima ejecución: Versión {global_session_V3.name_version_original.get()}: {estado}", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    ui.p(f"Horario de ejecución: {fecha}", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    #ui.p(f"Error: {self.mensaje.get() or default_message}", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    #ui.input_action_link(f"see_proces_{self.nombre}", "Ver porcentaje del proceso"),
                    ui.p(ui.output_ui(f"value_{self.nombre}"),  style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    ui.p( ui.output_ui(f"value_error_{self.nombre}"),  style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    
                    
                    class_="d-flex justify-content-between align-items-center w-100",
                ),
                ui.div(
                    ui.input_task_button(f"execute_{self.nombre}", f"Ejecutar"),
                ),
                
            )
        else:
            return ui.div("El archivo aún no se ha cargado. Por favor, cargue el archivo.")
        
        
        
        
    def existencia_modelo(self, modelo_boolean_value , base_datos, version_id=None, json_id=None,  nombre_version=None):
        """
        Valida si existe un modelo con un estado de ejecución dado en la base de datos
        y muestra un modal de advertencia si es necesario.

        :param base_datos: Ruta al archivo de la base de datos.
        :param version_id: ID de la versión a validar (opcional).
        :param json_id: ID del JSON a validar (opcional).
        :param nombre_modelo: Nombre del modelo a buscar.
        :param nombre_version: Versión a mostrar en el modal.
        :return: True si el modelo no existe o no tiene estado, False si existe y se muestra el modal.
        """
        # Verificar el estado de ejecución utilizando la función check_execution_status
        print(f"estoy pasando en esta funcion???: {version_id}, {json_id}")
        if not modelo_boolean_value:
            print("pase el boolean>")
            print(f"values now? {version_id}, {json_id}")
            estado_ejecucion = check_execution_status(base_datos, version_id=version_id, json_id=json_id)
            print(estado_ejecucion, "que estado hay aca?")
            if estado_ejecucion is not None and estado_ejecucion == "Exito":
                # Mostrar el modal de advertencia si el modelo ya tiene un estado de ejecución
                ui.modal_show(create_modal_warning_exist_model(self.nombre , nombre_version))
                return False  # El modelo ya existe con un estado asociado

            return True  # El modelo no existe o no tiene estado
