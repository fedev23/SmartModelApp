from shiny import reactive

class GlobalSessionModelo:
    def __init__(self):
        self.modelo_desarrollo_estado = reactive.Value("")
        self.modelo_desarrollo_hora = reactive.Value("")
        
        self.modelo_of_sample_estado = reactive.value("")
        self.modelo_of_sample_hora = reactive.value("")
        
        self.modelo_produccion_estado = reactive.value("")
        self.modelo_produccion_hora = reactive.value("")
        



global_session_modelos = GlobalSessionModelo()