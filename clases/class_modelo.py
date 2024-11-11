from clases.class_extact_time import global_fecha
from shiny import reactive, render, ui
from funciones.utils import  mover_files
import subprocess
import datetime
import asyncio
import traceback
from clases.reactives_name import global_names_reactivos


class ModeloProceso:
    def __init__(self, nombre, directorio, script_name, script_path, name_file, mensaje_id):
        self.nombre = nombre
        self.name_file = name_file
        self.mensaje_id = mensaje_id
        self.directorio = directorio
        self.script_name = script_name
        self.script_path = script_path
        self.proceso = reactive.Value(False)
        self.mensaje = reactive.Value("")
        self.click_counter = reactive.Value(0)  # Instancia de CargarDatos
        self.fecha_hora = reactive.Value("")
        self.extrat_hora = reactive.Value("")
        self.mensaje_error = reactive.Value("")
        
        
        

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
                read_stream(process.stdout, stdout, ""),
                read_stream(process.stderr, stderr, "")
            )

            # Esperar a que el proceso termine
            return_code = await process.wait()

            # Unir todas las lineas capturadas en un solo string
            stdout_output = '\n'.join(stdout)
            stderr_output = '\n'.join(stderr)

            return stdout_output, stderr_output, return_code 

        except Exception as e:
            print("Stacktrace:")
            traceback.print_exc()
            return None, str(e), 1
        
    async def ejecutar_proceso_prueba(self, click_count, mensaje, proceso):
        try:
            self.mensaje.set("En ejecución...")
            self.proceso.set(False)
            # Indicador de proceso en ejecución
            with ui.busy_indicators.use(spinners=True):
                # Ejecutar el script de manera asíncrona
                stdout, stderr, returncode = await self.run_script_prueba()

                # Verificar si hubo errores durante la ejecución
                if returncode != 0:
                    self.mensaje.set(f"Hubo un error en la ejecución.")
                    print(f"Salida del comando: {stdout}")
                else:
                    self.mensaje.set(f"Ejecución completada con éxito.")
                    self.proceso.set(True)
                    #origen = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida'
                    #salida = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada'
                    #mover = mover_files(origen, salida)
                    #print("movi a", mover)
                    

                return stdout, stderr 

        except Exception as e:
            print(f"Error en la ejecución: {e}")
            self.mensaje.set(f"Error en la ejecución: {str(e)}")
            return None, str(e), 1
        
    
    def acualizar_valor(self):
     if self.proceso.get():
         return True
     else:
         return False

    def mostrar_mensaje(self):
        # if self.proceso.get():
        return self.mensaje.get()

    def mostrar_boton_resultado(self):
        if self.proceso.get():
            return ui.input_action_link(f"open_html_{self.nombre}", f"Ver resultado de la etapa {self.nombre}")
        else:
            return None

    def log_fecha_hora(self):
        # Registra la fecha y hora actual
        now = datetime.datetime.now()
        # Formatear la fecha y hora para eliminar los milisegundos y microsegundos
        formatted_now = now.strftime('%Y-%m-%d %H:%M')
        self.fecha_hora = formatted_now
        return formatted_now

    def render_card(self, file_name, fecha_hora):
        default_message = "Aún no se ha ejecutado el proceso."
        if self.mensaje_error:
            self.mensaje = self.mensaje_error
        if file_name is not None:
            return ui.card(
                ui.card_header(
                    "",
                    ui.p(f"Nombre del archivo: {global_names_reactivos.get_name_file_db()}"),
                    ui.p(f"Fecha de última ejecución: {str(fecha_hora)}"),
                    ui.p(f"Estado: {self.mensaje.get() or default_message}"),
                    # ui.p(ui.output_text(self.mensaje_id)),
                    class_="d-flex justify-content-between align-items-center",
                ),
                ui.div(
                    ui.input_task_button(f"execute_{self.nombre}", f"Ejecutar {self.nombre}"),
                    self.mostrar_boton_resultado(),
                ),
            )
        else:
            return ui.div("El archivo aún no se ha cargado. Por favor, cargue el archivo.")

