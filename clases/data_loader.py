import asyncio
from shiny import ui, reactive
from clases.class_cargar_datos import CargarDatos

class DataLoader:
    def __init__(self, key):
        self.key = key
        self.proces_carga = reactive.Value(False)
        self.dataset = reactive.Value(None)
        self.name_reactive = reactive.Value(None)
        #self.file_name = reactive.Value(None)
    async def cargar_archivos(self, file_info, delimitador, directorio_validacion):
        print(f"Botón 'Cargar Datos' presionado en {self.key}.")

        if not file_info:
            print(f"No se seleccionó ningún archivo en {self.key}")
            raise ValueError("No se seleccionó ningún archivo")
        
        # Instanciar la clase CargarDatos
        cargador = CargarDatos(file_info, delimitador, directorio_validacion)

        # Mostrar el indicador de progreso
        with ui.Progress(min=1, max=19) as p:
            p.set(message="Cargando los datos a la tabla", detail="Puede tardar unos segundos...")
            for i in range(1, 16):
                p.set(i, message=f"Cargando los datos en la tabla de {self.key}")
                await asyncio.sleep(0.1)
                
            # Usar el método cargar_datos de la instancia CargarDatos
            df, file_name ,archivo_guardado = cargador.cargar_datos()
            print(f'Se ha guardado el archivo  {archivo_guardado} en {self.key}') # Mensaje de depuración
            self.proces_carga.set(True)
            self.dataset.set(df)
            self.name_reactive.set(file_name)
            return df, True
        
    def getDataset(self):
        return self.dataset.get()
    
    def getName(self):
        return self.name_reactive.get()
     
