from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from clases.global_session import global_session

user_id = global_session.obtener_id()
json_loader = LoadJson(user_id=user_id)
previous_values = json_loader.load_json()

data = [
    {"Nombre Nivel": "BajoBajo", "Regla": "score > 955", "Tasa de malos máxima": "3.0%"},
    {"Nombre Nivel": "BajoMedio", "Regla": "score > 930", "Tasa de malos máxima": "6.0%"},
    {"Nombre Nivel": "BajoAlto", "Regla": "score > 895", "Tasa de malos máxima": "9.0%"},
    {"Nombre Nivel": "MedioBajo", "Regla": "score > 865", "Tasa de malos máxima": "15.0%"},
    {"Nombre Nivel": "MedioMedio", "Regla": "score > 750", "Tasa de malos máxima": "18.0%"},
    {"Nombre Nivel": "Alto", "Regla": "score <= 750", "Tasa de malos máxima": "100.0%"}
]

opciones = {item["Nombre Nivel"]: f"{item['Regla']} - {item['Tasa de malos máxima']}" for item in data}

def param_in_sample(name_suffix):
    return ui.div(
        ui.row(
            ui.column(4, ui.input_text(f"par_vars_segmento_{name_suffix}", "Variables para reportes por Segmento")),
            ui.column(4, ui.input_selectize(
                f"par_rango_niveles",
                "Rango de la tabla de Niveles de Riesgo",
                choices=opciones,
                multiple=True
            )),
            ui.column(4, ui.input_text(f"par_rango_segmentos_{name_suffix}", "Rango de la tabla de Segmento"))
        ),
        ui.row(
            ui.column(4, ui.input_numeric(f"par_rango_reportes_{name_suffix}", "Rango de la tabla de Reportes", value=3)),
            ui.column(4, ui.input_numeric(f"par_cant_reportes_{name_suffix}", "Cantidad de reportes", value=100)),
            ui.column(4, ui.input_numeric(f"par_times_{name_suffix}", "Submuestras para bootstrap", value=25))
        ),
        #class_="custom-column"  
    )
 

     