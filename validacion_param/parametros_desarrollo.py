from shiny import App, reactive, render, ui
from funciones.utils import validar_columnas, validate_par_iv, process_target_col1, create_modal_parametros, id_buttons
from clases.loadJson import LoadJson
from global_var import global_data_loader_manager
import pandas as pd 
from funciones.utils_2 import cambiarAstring, trans_nulos_adic, validar_proyecto, mostrar_error
from clases.class_user_proyectName import global_user_proyecto

def server_parametros_desarrollo(input, output, session, name_suffix):
    # Obtener el DataLoader correspondiente basado en name_suffix, ya que necesita un key la clase dataloader
    data_loader = global_data_loader_manager.get_loader(name_suffix) 
    
    
    
         # Definir las funciones de transformación para cada input
    transformaciones = {
        'par_ids': cambiarAstring,
        'par_target': cambiarAstring,
        'cols_forzadas_a_predictoras': cambiarAstring,
        'par_var_grupo': cambiarAstring,
        'cols_nulos_adic': trans_nulos_adic,
        'cols_forzadas_a_cat': cambiarAstring,
        'cols_no_predictoras': cambiarAstring
    }

    
    
    def create_navigation_handler(input_id, screen_name, valid):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            if valid.get():
                await session.send_custom_message('navigate', screen_name)
    
    mensaje = reactive.Value("")  # Reactive value para el mensaje de error
    mensjae_error_proyecto = reactive.Value("")
    no_error = reactive.Value(True)
    count = reactive.value(0)
    
     

    @reactive.Effect
    @reactive.event(input[f'load_param_{name_suffix}'])
    def paramLoad():
        df = data_loader.getDataset()
        mensaje.set("")  # Limpia los mensajes anteriores
        mensjae_error_proyecto.set("")
        no_error.set(True)  # Restablece el estado de error a True

        # 1. Verificar si el dataset está vacío o es None
        if df is None:
            mensaje.set(f"No se seleccionó ningún archivo en {name_suffix}")
            no_error.set(False)
            return  # Detener ejecución aquí si no hay dataset

        # 2. Obtener el nombre del proyecto
        proyecto_nombre = global_user_proyecto.get_nombre_proyecto()
        # 4. Validar si el proyecto es válido
        validar = validar_proyecto(proyecto_nombre)
        if not validar:
            mensjae_error_proyecto.set(f"El proyecto '{proyecto_nombre}' no es válido. Por favor, selecciona o crea uno válido en {name_suffix}")
            no_error.set(False)
            return  # Detener ejecución si el proyecto no es válido

        # Si pasa las validaciones de archivo y proyecto, continuar con las validaciones de columnas

        # 5. Acumular los errores relacionados con la validación de columnas
        error_messages = []

        # Validación de columnas identificadoras
        resultado_id = validar_columnas(df, input[f'par_ids']())
        if resultado_id is not False:
            error_messages.append(f"Columnas identificadoras: no puede estar vacio en {name_suffix}")

        # Validación del parámetro IV
        resultado_iv = validate_par_iv(input[f'par_iv']())
        if resultado_iv is  False:
            error_messages.append(f"Error al descartar variables por bajo IV: {resultado_iv}")

        # Validación de la columna target
        target_col_value = input[f'par_target']()
        resultado_target = process_target_col1(target_col_value)
        print(resultado_target)
        if resultado_target is False:
            error_messages.append(f"La columna target es obligatoria para la generación del modelo {name_suffix}")

        # Validación del parámetro Training and Testing
        training = input[f'par_split']()
        if training is None:
            error_messages.append(f"El parámetro Training and Testing en la muestra {name_suffix} debe tener un valor")
        elif training > 2 or training < 0:
            error_messages.append(f"El valor de Training and Testing en la muestra {name_suffix} no puede ser mayor que 2 ni menor que 0.")

        # Mostrar todos los errores de columnas juntos, si los hay
        if error_messages:
            mensaje.set("\n".join(error_messages))
            no_error.set(False)
            return  # Detener ejecución si hay errores en las columnas

        # Si no hay errores, limpiar el mensaje y proceder
        mensaje.set("")  # Limpia el mensaje de error
        no_error.set(True)  # Indicar que no hay errores
        create_navigation_handler(f'load_param_{name_suffix}', 'Screen_3', no_error)

        # ABRO EL ACORDEON PARA QUE LA REDIRECCION SEA POR AHI
        ui.update_accordion("my_accordion", show=["desarrollo"])

        # Ejecutar acciones adicionales
        inputs_procesados = {key: transformacion(input[key]()) for key, transformacion in transformaciones.items()}
        load_handler = LoadJson(input)
        load_handler.inputs.update(inputs_procesados)
        json_file_path = load_handler.loop_json()
        print(f"Inputs guardados en {json_file_path}")

        return True


    
    
    @output
    @render.text
    def error_proyecto():
        return mostrar_error(mensjae_error_proyecto.get())
          
    @output
    @render.text
    def error():
      return mostrar_error(mensaje.get())
               
    
   
    
    ##ES IMPORTANTE USAR ESTA FUNCION Y DECLARAR EL PARAMETO QUE LE CORRESPONDE, PARA ACTUALIZAR EL UI DE SELECCIONADOR
    # ESTO FUNCIONA ASI: ACTUALIZA EL VALOR UNA VEZ DELCARADO PARA QUE RECONOZCA LAS COLUMNAS
    ## SI DECLARAMOS UN NUEVO PARAMETRO QUE SEA SELECCIONADOR NO VA A FUNCION SI NO LO ADJUTAMOS DEBAJO EN EL  ui.update_selectize
    @reactive.Effect
    def update_column_choices():
        # Load the DataFrame and get its columns
        df = data_loader.getDataset()  # Ensure you're fetching the DataFrame from the data loader

        if isinstance(df, pd.DataFrame) and not df.empty:
            column_names = df.columns.tolist() 
        else:
            column_names = []

        # Update the selectize input with the columns from the DataFrame
        ui.update_selectize("par_ids", choices=column_names)
        ui.update_selectize("cols_forzadas_a_predictoras", choices=column_names)
        ui.update_selectize("cols_forzadas_a_cat", choices=column_names)
        ui.update_selectize("par_var_grupo", choices=column_names)
        ui.update_selectize("par_target", choices=column_names)
        ui.update_selectize("cols_no_predictoras", choices=column_names)
        ui.update_selectize("cols_nulos_adic", choices=column_names)
        ui.update_selectize("par_vars_segmento", choices=column_names)
        
        
   

    
    
    
   
    
    
