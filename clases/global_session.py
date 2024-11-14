from shiny import reactive

class GlobalSession:
    def __init__(self):
        self.session_state = reactive.Value({"is_logged_in": False, "id": None})
        self.proceso = reactive.Value(False)
        self.id_proyecto = reactive.Value(None) 
        self.proyecto_seleccionado = reactive.Value(None) 
        self.id_user =  reactive.Value(None)    
        self.id_version = reactive.Value(None)
        self.id_dataSet = reactive.Value(None)
        self.proyecto_nombre = reactive.Value(None)
        self.proyecto_seleccionado_id = reactive.Value(None)
        self.path_guardar_dataSet_en_proyectos = reactive.Value(None)
        self.proyectos_usuarios = reactive.Value(None)
        self.versiones_name = reactive.Value(None)
        
        
    def actualizar_directorio(self, nuevo_directorio):
        if self.proceso.get() is True:
            self.directorio = nuevo_directorio
            
    def set_id_proyect(self, id):
        self.id_proyecto.set(id)
    
    def get_id_proyecto(self):
        return self.id_proyecto.get() 
    
    def set_id_dataSet(self, id):
        self.id_dataSet.set(id)
    
    def get_id_dataSet(self):
        return self.id_dataSet.get()  
    
    def set_id_version(self, id):
        self.id_version.set(id)
    
    def get_id_version(self):
        return self.id_version.get()  
    
    def set_id_user(self, id):
        self.id_user.set(id)
    
    def get_id_user(self):
        return self.id_user.get()   
    
    def set_proyecto_seleccionado(self, id):
        self.proyecto_seleccionado.set(id)
    
    def get_proyecto_seleccionado(self):
        return self.proyecto_seleccionado.get()  
    
    
    def set_name_proyecto(self, id):
        self.proyecto_nombre.set(id)
    
    def get_name_proyecto(self):
        return self.proyecto_nombre.get()  
    
    def set_proyecto_seleccionado_id(self, id):
        self.proyecto_seleccionado_id.set(id)
    
    def get_proyecto_seleccionado_id(self):
        return self.proyecto_seleccionado_id.get()    
    
    
    def set_path_guardar_dataSet_en_proyectos(self, id):
        self.path_guardar_dataSet_en_proyectos.set(id)
    
    def get_path_guardar_dataSet_en_proyectos(self):
        return self.path_guardar_dataSet_en_proyectos.get()  
    
    def set_proyectos_usuarios(self, id):
        self.proyectos_usuarios.set(id)
    
    def get_proyectos_usuarios(self):
        return self.proyectos_usuarios.get()   
    
    
    def set_versiones_name(self, name):
        self.versiones_name.set(name)
    
    def get_versiones_name(self):
        return self.versiones_name.get()   
    
    
    
    
    
         
            
    def obtener_id(self):
        @reactive.Effect  # Coloca el decorador aquí, fuera de la función interna
        def user_id():
            # Función para obtener el ID si el proceso está activo y el usuario está logueado
            if  self.proceso.get():
                print("pase en global session")
                state = self.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"]
                    user_id_cleaned = user_id.replace('|', '_')
                    print("tengo el id", user_id_cleaned)
                    return user_id
            return None  # Devuelve None si el proceso no está activo o el usuario no está logueado

# Instancia de GlobalSession
global_session = GlobalSession()