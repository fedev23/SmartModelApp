from shiny import reactive

class GlobalSessionV2:
    def __init__(self):
        self.id_Data_validacion_sc = reactive.Value("")
        self.data_reactivo_validacion_sc = reactive.Value(None)
        self.opciones_name_dataset_Validation_sc = reactive.Value()
        self.nombre_dataset_validacion_sc = reactive.Value()
        self.lista_nombre_datos_validacion_Sc = reactive.Value()
        self.json_desarrollo = reactive.Value()
        self.retornado = reactive.Value(False)
        self.retorne_niveles =  reactive.Value(False)
        

    def set_id_Data_validacion_sc(self, id):
        self.id_Data_validacion_sc.set(id)
    
    def get_id_Data_validacion_sc(self):
        return self.id_Data_validacion_sc.get() 
    
    def set_data_set_reactivo_validacion_sc(self, dataSet):
        self.data_reactivo_validacion_sc.set(dataSet)
    
    def get_data_reactivo_validacion_sc(self):
        return self.data_reactivo_validacion_sc.get() 
    
    def set_opciones_name_dataset_Validation_sc(self, id):
        self.opciones_name_dataset_Validation_sc.set(id)
    
    def get_opciones_name_dataset_Validation_sc(self):
        return self.opciones_name_dataset_Validation_sc.get() 
    
    def set_nombre_dataset_validacion_sc(self, name):
        self.nombre_dataset_validacion_sc.set(name)
    
    def get_nombre_dataset_validacion_sc(self):
        return self.nombre_dataset_validacion_sc.get() 
    
    def set_lista_nombre_datos_validacion_Sc(self, lista):
        self.lista_nombre_datos_validacion_Sc.set(lista)
    
    def get_lista_nombre_datos_validacion_Sc(self):
        return self.lista_nombre_datos_validacion_Sc.get() 
    
    def set_json_params_desarrollo(self, json):
        self.json_desarrollo.set(json)
        
      
    def get_json_params_desarrollo(self):
        return self.json_desarrollo.get()
    
    
    def set_retornado(self, json):
        self.retornado.set(json)
        
      
    def get_retornado(self):
        return self.retornado.get()
    
    
    def set_retorne_niveles(self, json):
        self.retorne_niveles.set(json)
        
      
    def get_retorne_niveles(self):
        return self.retorne_niveles.get()
    
    



global_session_V2 = GlobalSessionV2()