from shiny import reactive, render, ui
from funciones.utils import validar_columnas, validate_par_iv, process_target_col1, validate_null, validate_binary_values
from funciones.utils_2 import cambiarAstring
from clases.global_session import *

class Validator:
    def __init__(self, input, df, name_suffix):
        self.input = input
        self.df = df
        self.name_suffix = name_suffix
        self.error_messages = []

    def validate_column_identifiers(self):
        resultado_id = validar_columnas(self.df, self.input[f'par_ids']())
        if resultado_id is not False:
            self.error_messages.append(f"Columnas identificadoras: no puede estar vacio en {self.name_suffix}")

    def validate_iv(self):
        resultado_iv = validate_par_iv(self.input[f'par_iv']())
        if resultado_iv is False:
            self.error_messages.append(f"Error al descartar variables por bajo IV: {resultado_iv}")
        
    

    def validate_target_column(self):
        target_col_value = self.input[f'par_target']()
        print(target_col_value, "valor de target, que pasa?")
        resultado_target = process_target_col1(target_col_value)
        #target_col_value = cambiarAstring(target_col_value)
        if resultado_target is False:
            self.error_messages.append(f"La columna target es obligatoria para la generación del muestra {self.name_suffix}")

        tiene_nulls = validate_null(target_col_value, self.df)
        if tiene_nulls:
            self.error_messages.append(f"La columna target no puede contener valores nulos en la muestrea {self.name_suffix}")
            
        valores_distintos_univocos =  validate_binary_values(target_col_value, global_session.get_data_set_reactivo())
        if valores_distintos_univocos:
            self.error_messages.append(f"La columna target no puede contener valores distintos de 0 y 1 {self.name_suffix}")
            

        
        
    def validate_training_split(self):
        training = self.input[f'par_split']()
        if training is None:
            self.error_messages.append(f"El parámetro Training and Testing en la muestra {self.name_suffix} debe tener un valor")
        elif training > 2 or training < 0:
            self.error_messages.append(f"El valor de Training and Testing en la muestra {self.name_suffix} no puede ser mayor que 2 ni menor que 0.")

    def get_errors(self):
        return self.error_messages

    def is_valid(self):
        return len(self.error_messages) == 0

    def clear_errors(self):
        self.error_messages = []
