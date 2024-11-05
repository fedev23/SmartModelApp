from shiny import reactive, render, ui
import pandas as pd
import os
from global_var import global_data_loader_manager
from clases.global_name import global_name_manager
from clases.global_modelo import modelo_of_sample, modelo_produccion, global_desarollo
from clases.data_loader import DataLoader
from clases.global_reactives import global_estados


class ScreenClass():
    def __init__(self, directorio, name_suffix):
        # super().__init__(name_suffix)  # Llamar al constructor de la clase padre
        self.input = input
        self.name = name_suffix
        self.modelo = modelo_of_sample
        self.modelo_produccion = modelo_produccion
        self.global_desarollo = global_desarollo
        self.data_loader = global_data_loader_manager.get_loader(name_suffix)
        self.directorio = directorio
        self.mensaje_Error = reactive.Value("")
        self.proceso_a_completado = reactive.Value(False)
        self.nombre_archivo = reactive.Value(None)
        self.error_messages = []
        self.hay_errores = reactive.Value(False)
        

    # ESTA FUNCION SE CREA CON EL FIN DE CAMBIAR EL NOMBRE DEL ARCHIVO QUE INGRESA AL USER, ESTO ES. PARA QUE DEPENDE EL
    # CUADERNO A EJECUTAR LEA EL ARCHVIO HARDCODE DE SMART MODEL

    def cambiar_name(self, nuevo_nombre_archivo, file_info):
        # Obtén la ruta completa del archivo original
        nombre_archivo_a_editar = file_info[0]['datapath']

        # Define el nuevo nombre del archivo
        nuevo_nombre_archivo = nuevo_nombre_archivo
        nuevo_nombre_archivo_completo = os.path.join(
            os.path.dirname(nombre_archivo_a_editar), nuevo_nombre_archivo)

        # Renombra el archivo original con el nuevo nombre
        os.rename(nombre_archivo_a_editar, nuevo_nombre_archivo_completo)

        # Actualiza 'name' con solo el nombre del archivo y 'datapath' con la ruta completa
        # Solo el nombre del archivo
        file_info[0]['name'] = nuevo_nombre_archivo
        file_info[0]['datapath'] = nuevo_nombre_archivo_completo

# esta funcion esta divida en dos sobre la clase padre, este clae hereda de dataloader sus metodos
  # FUNCION QUE SE UTILIZA PARA CARGAR DATOS EN TODOS LOS SERVIDORES O SEA CARGA LOS DATOS DE DESAROLLO, IN SAMPLE ETC..
    async def load_data(self, file_func, name_suffix):
        try:
            file_info = file_func()
            if file_info is None or len(file_info) == 0:
                self.error_messages.append(
                    "No se ha seleccionado ningún archivo.")
                self.hay_errores.set(True)
                raise ValueError(
                    "No se ha seleccionado ningún archivo. Busque el archivo y luego presione cargar datos.")
            else:
                self.hay_errores.set(False)
            name = file_info[0]
            nombre_archivo = name['name']
            # DEPENDE CUAL SEA EL NOMBRE DE LA ETAPA SETEA EL NOMBRE PARA LUEGO UTILIZARLO
            if name_suffix == 'validacion':
                self.nombre_archivo.set(nombre_archivo)
                global_name_manager.set_file_name_validacion(nombre_archivo)
                self.modelo.name_file = nombre_archivo
                nuevo_nombre_archivo = "Muestra_Validación.txt"
                self.cambiar_name(nuevo_nombre_archivo,file_info)
            elif name_suffix == 'produccion':
                self.nombre_archivo.set(nombre_archivo)
                global_name_manager.set_file_name_produccion(nombre_archivo)
                nuevo_nombre_archivo = "Muestra_Scoring.txt"
                self.cambiar_name(nuevo_nombre_archivo, file_info)
                self.modelo_produccion.name_file = nombre_archivo
            elif name_suffix == 'desarrollo':
                self.nombre_archivo.set(nombre_archivo)
                global_name_manager.set_file_name_desarrollo(nombre_archivo)
                self.global_desarollo.name_file = nombre_archivo
                # RENOMBRO EL ARCHIVO ASI LO LEE SMARTMODEL
                nuevo_nombre_archivo = "Muestra_Desarrollo.txt"
                self.cambiar_name(nuevo_nombre_archivo, file_info)
            elif name_suffix == 'in_sample':
                self.nombre_archivo.set(nombre_archivo)
                global_name_manager.set_file_name_desarrollo(nombre_archivo)
                self.global_desarollo.name_file = nombre_archivo

            if self.error_messages:
                self.mensaje_Error.set("\n".join(self.error_messages))
            else:
                # Obtener delimitador y cargar datos
                await self.data_loader.cargar_archivos(file_info, self.directorio)
                self.error_messages.clear()  # Limpiar errores después de la carga exitosa
                self.proceso_a_completado.set(True)
                return nombre_archivo

        except ValueError as e:
            self.mensaje_Error.set("\n".join(self.error_messages))
            print(f"Error: {e}")
        except Exception as e:
            self.mensaje_Error.set("Ocurrió un error inesperado.")
            print(f"Error inesperado en clase screens.py: {e}")

    def render_error_message(self, name_suffix):
        if self.proceso_a_completado.get() is False:
            self.hay_errores.set(True)
            self.mensaje_Error.set(
                f"Seleccione un archivo para continuar en {name_suffix}")
            ui.notification_show(
                ui.p(f"Error:", style="color: red;"),
                action=ui.p(self.mensaje_Error.get(),
                            style="font-style: italic;"),
                duration=None,
                close_button=True
            )

    def render_data_summary(self):
        df = self.data_loader.getDataset()  # Usar el método heredado
        if df is not None and not df.empty:
            select_number_data_set = int(global_estados.get_numero_dataset())
            # Devuelve un resumen de los primeros 5 registros
            return pd.DataFrame(df.head(select_number_data_set))

    def render_button(self):
        if self.proceso_a_completado.get():
            return ui.input_action_button("ir_ejecucion_validacion_out_to", "Ir a ejecución")
        return ui.TagList()
