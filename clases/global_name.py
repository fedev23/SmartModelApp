from shiny import reactive

class GlobalName:
    def __init__(self):
        self.name_file_validacion = reactive.Value(None)  # Variable reactiva para almacenar el nombre del archivo de validación
        self.name_file_produccion = reactive.Value(None)  # Variable reactiva para almacenar el nombre del archivo de producción
        self.name_file_desarrollo = reactive.Value(None)  # Variable reactiva para almacenar el nombre del archivo de desarrollo
        self.name_file_validacion_in_sample =  reactive.Value(None) 
        self.name_file = reactive.Value(None) 
        
         
        
    def set_name_file(self, file_name):
        """Establece el nombre del archivo en la variable reactiva."""
        self.name_file.set(file_name)
    
    def get_name_file(self):
        """Obtiene el nombre del archivo de la variable reactiva."""
        return self.name_file.get()
        
    def set_name_in_sample(self, file_name):
     self.name_file_validacion_in_sample(file_name)
     
    
    def get_name_in_sample(self):
     return self.name_file_validacion_in_sample.get()

    def set_file_name_validacion(self, file_name):
        self.name_file_validacion.set(file_name)  # Asigna el nombre del archivo de validación

    def get_file_name_validacion(self):
        return self.name_file_validacion.get()  # Devuelve el nombre del archivo de validación
    
    def set_file_name_produccion(self, file_name):
        self.name_file_produccion.set(file_name)  # Asigna el nombre del archivo de producción

    def get_file_name_produccion(self):
        return self.name_file_produccion.get()  # Devuelve el nombre del archivo de producción
    
    def set_file_name_desarrollo(self, file_name):
        self.name_file_desarrollo.set(file_name)  # Asigna el nombre del archivo de desarrollo

    def get_file_name_desarrollo(self):
        return self.name_file_desarrollo.get()  # Devuelve el nombre del archivo de desarrollo

# Crear una instancia global de GlobalName
global_name_manager = GlobalName()
