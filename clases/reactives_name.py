from shiny import reactive


class Reactividad:
    def __init__(self):
        self.name_desarrollo = reactive.Value(None)
        self.name_produccion = reactive.Value(None)
        self.name_validacion_in_sample = reactive.Value(None)
        self.name_validacion_of_to_sample = reactive.Value(None)
        self.fecha_produccion = reactive.Value(None)
        self.file_name = reactive.Value(None)
        self.name_file_db = reactive.Value(None)
        self.name_data_Set = reactive.Value(None)
        self.proceso_leer_dataset = reactive.Value(False)


    def set_file_name(self, name):
        # Actualiza el valor de fechaHora usando el método set()
        self.file_name.set(name)

    def get_file_name(self):
        return self.file_name.get()
    
    ##NOMBRE DEL DATA SET QUE ENTRA POR INPUT DESARROLLO
    def set_name_data_Set(self, name):
        # Actualiza el valor de fechaHora usando el método set()
        self.file_name.set(name)

    def get_name_data_Set(self):
        return self.file_name.get()
    
    
    ##PROCESO PARA QUE SE EJECUTE LA FUCION LEER_DATASET
    def set_proceso_leer_dataset(self, boolean):
        self.proceso_leer_dataset.set(boolean)

    def get_proceso_leer_dataset(self):
        return self.proceso_leer_dataset.get()

    
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
    
    def set_name_file_db(self, name):
     self.name_file_db.set(name)
 
    def get_name_file_db(self):
        return self.name_file_db.get()
    
  
    

global_names_reactivos = Reactividad()

