
from shiny import reactive, render, ui
from clases.global_session import *
from datetime import datetime
import asyncio
import traceback
from clases.reactives_name import global_names_reactivos
from api.db import *
from funciones_modelo.global_estados_model import global_session_modelos
from clases.global_sessionV2 import *



class ModeloProceso:
    def __init__(self, nombre, directorio, script_name, script_path, name_file, mensaje_id, hora, estado):
        self.nombre = nombre
        self.name_file = name_file
        self.mensaje_id = mensaje_id
        self.directorio = directorio
        self.hora = hora
        self.estado = estado
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
        
        
        
    async def run_script_prueba(self):
        # Convertir la ruta de Windows a WSL
        wsl_directorio = self.directorio
        comando = f'cd {wsl_directorio} && {self.script_path}'
        print(f"Comando a ejecutar: {comando}")

        try:
            # Crear el proceso de forma asíncrona
            process = await asyncio.create_subprocess_shell(
                comando,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Capturar la salida y los errores en tiempo real
            stdout, stderr = [], []

            async def read_stream(stream, output_list, output_prefix):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    output_list.append(line.decode('utf-8').strip())
                    print(f"{output_prefix}: {output_list[-1]}")

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

            return stdout_output, stderr_output, return_code, error_message

        except Exception as e:
            # Capturar cualquier excepción y devolver el mensaje de error
            error_message = f"Excepción durante la ejecución: {str(e)}"
            print("Stacktrace:")
            traceback.print_exc()
            return None, None, 1, error_message

    async def ejecutar_proceso_prueba(self, click_count, mensaje, proceso):
        try:
            # Obtener valores de fuentes reactivas antes de la tarea extendida
            
            # Mostrar mensaje inicial
            self.mensaje.set("En ejecución...")
            #proceso(False)

            # Indicador de proceso en ejecución
            with ui.busy_indicators.use(spinners=True):
                # Ejecutar el script de manera asíncrona
                stdout, stderr, returncode, error_message = await self.run_script_prueba()

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
            #fecha = self.log_fecha_hora()
            return ui.card(
                ui.card_header(
                    "",
                    ui.p(f"Nombre del archivo: {file_name}", style="margin: 0; line-height: 1.5; vertical-align: middle;"), 
                    #ui.p(f"Fecha de última ejecución: {str(fecha_hora)}"),
                    ui.p(f"Estado de la ultima ejecución:{global_session.get_versiones_name()}: {estado}", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    ui.p(f"Horario de ejecución: {fecha}", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    ui.p(f"Estado: {self.mensaje.get() or default_message} ", style="margin: 0; line-height: 1.5; vertical-align: middle;"),
                    # ui.p(ui.output_text(self.mensaje_id)),
                    class_="d-flex justify-content-between align-items-center w-100",
                ),
                ui.div(
                    ui.input_task_button(f"execute_{self.nombre}", f"Ejecutar"),
                ),
                
            )
        else:
            return ui.div("El archivo aún no se ha cargado. Por favor, cargue el archivo.")

    
    
   