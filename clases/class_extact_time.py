import datetime
from shiny import reactive


class ProcesTime:
    def __init__(self):
        self.fechaHora = reactive.Value(None)
        self.fecha_in_sample = reactive.Value(None)
        self.fecha_of_to_sample = reactive.Value(None)
        self.fecha_produccion = reactive.Value(None)

    def set_fecha_desarrollo(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fechaHora.set(fecha_hora)

    def get_fecha_desarrollo(self):
        return self.fechaHora.get()

    def set_fecha_in_sample(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fecha_in_sample.set(fecha_hora)

    def get_fecha_in_sample(self):
        return self.fecha_in_sample.get()
    
    def set_fecha_of_to_Sample(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fecha_of_to_sample.set(fecha_hora)

    def get_fecha_of_to_Sample(self):
        return self.fecha_of_to_sample.get()
    
    def set_fecha_produccion(self, fecha_hora):
        # Actualiza el valor de fechaHora usando el método set()
        self.fecha_produccion.set(fecha_hora)

    def get_fecha_produccion(self):
        return  self.fecha_produccion.get()


global_fecha = ProcesTime()
