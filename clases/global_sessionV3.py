from shiny import reactive

class GlobalSessionV3:
    def __init__(self):
        self.name_proyecto_original = reactive.Value()
        self.name_version_original =  reactive.Value()
        self.name_version_niveles_score_original = reactive.Value()
        
        

global_session_V3 = GlobalSessionV3()