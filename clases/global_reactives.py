from shiny import reactive


class Reactividad:
    def __init__(self):
        self.proceso = reactive.Value(False)
        self.error = reactive.Value(False)
        self.fecha_in_sample = reactive.Value(None)
        self.fecha_of_to_sample = reactive.Value(None)
        self.fecha_produccion = reactive.Value(None)
        self.numero_de_dataset =  reactive.Value("5")
        self._delimitador = None
        self.mensaje_por_defecto = reactive.Value()

    def set_process_desarrollo(self, proceso):
        # Actualiza el valor de fechaHora usando el método set()
        self.proceso.set(proceso)

    def get_estado_desarrollo(self):
        return self.proceso.get()
    
    def set_error_desarrollo(self, error):
     self.error.set(error)
 
    def get_error_desarrollo(self):
        return self.error.get()
    
     
    def set_mensaje_desarrollo(self, mensaje):
     self.error.set(mensaje)
 
    def get_mensaje_desarrollo(self):
        return self.error.get()
    
    
    def set_numero_dataset(self, numero_de_dataset):
     self.numero_de_dataset.set(numero_de_dataset)
 
    def get_numero_dataset(self):
        return self.numero_de_dataset.get()
    
    
    def set_delimitador(self, delimitador):
        self._delimitador = delimitador

    def get_delimitador(self):
        return self._delimitador
    
    def set_mensaje_por_defecto(self, mensaje):
        self.mensaje_por_defecto = mensaje

    def get_mensaje_por_defecto(self):
        return self.mensaje_por_defecto
    
    
    

global_estados = Reactividad()

