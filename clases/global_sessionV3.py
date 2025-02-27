from shiny import reactive

class GlobalSessionV3:
    def __init__(self):
        self.name_proyecto_original = reactive.Value()
        self.name_version_original =  reactive.Value()
        self.name_version_niveles_score_original = reactive.Value(None)
        self.modelo_existe = reactive.Value(False)
        self.id_validacion_scoring = reactive.Value(None)
        self.id_score = reactive.Value(None)
        self.json_params_insa = reactive.Value(None)
        
        

global_session_V3 = GlobalSessionV3()