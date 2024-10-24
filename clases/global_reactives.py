from shiny import reactive


class Reactividad:
    def __init__(self):
        self.proceso = reactive.Value(False)
        self.error = reactive.Value(False)
        self.fecha_in_sample = reactive.Value(None)
        self.fecha_of_to_sample = reactive.Value(None)
        self.fecha_produccion = reactive.Value(None)

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
    

global_estados = Reactividad()

