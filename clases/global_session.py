from shiny import reactive

class GlobalSession:
    def __init__(self):
        self.session_state = reactive.Value({"is_logged_in": False, "id": None})
        self.proceso = reactive.Value(False)
        self.id_proyecto = reactive.Value(None) 
        self.proyecto_seleccionado = reactive.Value(None) 
        self.id_user =  reactive.Value(None)    
    def actualizar_directorio(self, nuevo_directorio):
        if self.proceso.get() is True:
            self.directorio = nuevo_directorio
            
    def set_id_proyect(self, id):
        self.id_proyecto.set(id)
    
    def get_id_proyecto(self):
        return self.id_proyecto.get()  
    
    def set_id_user(self, id):
        self.id_proyecto.set(id)
    
    def get_id_user(self):
        return self.id_proyecto.get()   
    
    def set_proyecto_seleccionado(self, id):
        self.proyecto_seleccionado.set(id)
    
    def get_proyecto_seleccionado(self):
        return self.proyecto_seleccionado.get()       
            
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
