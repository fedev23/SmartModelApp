from clases.data_loader import DataLoader

class GlobalDataLoaderManager:
    def __init__(self):
        self.loaders = {
            "desarrollo": DataLoader(key="desarrollo"),
            "produccion": DataLoader(key="produccion"),
            "in_sample": DataLoader(key="in_sample"),
             "validacion": DataLoader(key="validacion")
        }

    def get_loader(self, key):
        return self.loaders.get(key)

# Crear una instancia global del gestor de datos
global_data_loader_manager = GlobalDataLoaderManager()
