from shiny import reactive


class Reactividad:
    def __init__(self):
        self.name_desarrollo = reactive.Value(None)
        self.name_produccion = reactive.Value(None)
        self.name_validacion_in_sample = reactive.Value(None)
        self.name_validacion_of_to_sample = reactive.Value(None)
        self.fecha_produccion = reactive.Value(None)

    def name_desarrollo_set(self, name):
        # Actualiza el valor de fechaHora usando el método set()
        self.name_desarrollo.set(name)

    def name_desarrollo_get(self):
        return self.name_desarrollo.get()
    
    def name_produccion_set(self, name):
     self.name_produccion.set(name)
 
    def name_produccion_get(self):
        return self.name_produccion.get()
    
    def name_validacion_in_sample_set(self, name):
     self.name_validacion_in_sample.set(name)
 
    def name_validacion_in_sample_get(self):
        return self.name_validacion_in_sample.get()
    
    def name_validacion_of_to_sample_set(self, name):
     self.name_validacion_of_to_sample.set(name)
 
    def name_validacion_of_to_sample_get(self):
        return self.name_validacion_of_to_sample.get()
    
  
    

global_names_reactivos = Reactividad()

