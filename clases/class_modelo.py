
from shiny import reactive, render, ui
from funciones.utils import  mover_file_reportes_puntoZip
from clases.global_session import *
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
        self.click_counter = reactive.Value(0)
        self.fecha_hora = reactive.Value("")
        self.extrat_hora = reactive.Value("")
        self.mensaje_error = reactive.Value("")

    async def run_script_prueba(self):
        """
        Ejecuta un script en un entorno WSL y captura salida.
        """
        wsl_directorio = self.directorio
        comando = f'cd {wsl_directorio} && {self.script_path}'
        print(f"Comando a ejecutar: {comando}")

        try:
            process = await asyncio.create_subprocess_shell(
                comando,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = [], []

            async def read_stream(stream, output_list, prefix):
                while True:
                    line = await stream.readline()
                    if not line:
                        break
                    output_list.append(line.decode('utf-8').strip())
                    print(f"{prefix}: {output_list[-1]}")

            await asyncio.gather(
                read_stream(process.stdout, stdout, "STDOUT"),
                read_stream(process.stderr, stderr, "STDERR")
            )

            return_code = await process.wait()
            return '\n'.join(stdout), '\n'.join(stderr), return_code
        except Exception as e:
            print("Error ejecutando script:")
            traceback.print_exc()
            return None, str(e), 1

    async def ejecutar_proceso_prueba(self, click_count, mensaje, proceso):
        """
        Ejecuta el proceso principal, maneja errores y realiza tareas asociadas como mover archivos.
        """
        try:
            self.mensaje.set("En ejecución...")
            self.proceso.set(False)

            with ui.busy_indicators.use(spinners=True):
                stdout, stderr, returncode = await self.run_script_prueba()

                if returncode != 0:
                    self.mensaje.set("Hubo un error en la ejecución.")
                    print(f"STDOUT: {stdout}")
                    print(f"STDERR: {stderr}")
                else:
                    self.mensaje.set("Ejecución completada con éxito.")
                    self.proceso.set(True)

                    # Mover archivo generado (ZIP u otros)
                    self.mover_modelo_generado()

                return stdout, stderr
        except Exception as e:
            print(f"Error en la ejecución: {e}")
            self.mensaje.set(f"Error en la ejecución: {str(e)}")
            return None, str(e), 1

    def mover_modelo_generado(self):
        """
        Mueve el modelo generado (.zip) al destino correspondiente.
        """
        origen = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/Reportes'
        destino = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'

        try:
            resultado = mover_file_reportes_puntoZip(origen, destino)
            print(f"Modelo movido correctamente: {resultado}")
        except Exception as e:
            print(f"Error moviendo modelo: {e}")
            self.mensaje_error.set(f"Error moviendo modelo: {str(e)}")

    def log_fecha_hora(self):
        now = datetime.datetime.now()
        self.fecha_hora = now.strftime('%Y-%m-%d %H:%M')
        return self.fecha_hora

    def render_card(self, file_name):
        default_message = "Aún no se ha ejecutado el proceso."
        mensaje_actual = self.mensaje.get() or default_message

        return ui.card(
            ui.card_header(
                "",
                ui.p(f"Nombre del archivo: {file_name}"),
                ui.p(f"Estado: {mensaje_actual}"),
                class_="d-flex justify-content-between align-items-center",
            ),
            ui.div(
                ui.input_task_button(f"execute_{self.nombre}", f"Ejecutar {self.nombre}"),
                self.mostrar_boton_resultado(),
            ),
        )

    def mostrar_boton_resultado(self):
        if self.proceso.get():
            return ui.input_action_link(f"open_html_{self.nombre}", f"Ver resultado de la etapa {self.nombre}")
        return None
