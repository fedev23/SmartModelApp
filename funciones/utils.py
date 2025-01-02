import os
from shiny import App, ui, reactive

import zipfile

import os
import shutil


# configurar_event_loop(): Esta función verifica si el sistema operativo es Windows y, en ese caso,
# cambia el bucle de eventos a ProactorEventLoop, que es necesario para manejar subprocesos asíncronos en Windows.


def mover_file_reportes_puntoZip(origen: str, destino: str, nombre_archivo: str = "modelo.zip"):
    ruta_archivo = os.path.join(origen, nombre_archivo)

    # Verificar si el archivo existe
    if os.path.isfile(ruta_archivo):
        print(f"Archivo encontrado: {ruta_archivo}")

        # Construir la nueva ruta de destino
        nueva_ruta = os.path.join(destino, nombre_archivo)

        # Mover el archivo al destino
        shutil.copy(ruta_archivo, nueva_ruta)
        print(f"Archivo movido a: {nueva_ruta}")

        # Devolver la nueva ruta del archivo
        return nueva_ruta, True
    else:
        error_msg = f"El archivo {nombre_archivo} no se encontró en la carpeta {origen}."
        print(error_msg)
        return error_msg


def validar_columnas(df, nombre_input):
    nombre_input = str(nombre_input)
    nombre_input = nombre_input[1:-1].replace("'", "").strip()
    nombre_input = nombre_input.split(',')
    for column in nombre_input:
        if column.strip() in df.columns:
            print("ok", column)
            return False
        else:
            mensaje = (
                f"error en el parametro '{nombre_input}',  '{column}' no encontrada.")
            return mensaje

        return False


def create_zip_from_directory(directory_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(directory_path):
            for file in files:
                # Excluir archivos que comiencen con `~$`
                if not file.startswith('~$'):
                    file_path = os.path.join(root, file)
                    try:
                        zipf.write(file_path, os.path.relpath(
                            file_path, directory_path))
                    except PermissionError as e:
                        print(
                            f"Error de permiso al intentar leer el archivo: {file_path}")


def process_target_col(df, target_col):
    target_col = input.target_col().split(',')
    if all(isinstance(element, str) and element.strip() == '' for element in target_col):
        return True
    else:
        return False


def process_target_col1(target_col):
    if not target_col:  # Esto verifica si está vacío o None
        return False
    # Aquí puedes agregar más lógica de validación si es necesario
    return True  #


def validate_null(target_col, df):
    if df[target_col].isnull().any():
        print(f"La columna '{target_col}' tiene valores nulos.")
        return True



def validate_par_iv(value):
    if value > 10 or value < 0.5:
        return False
    else:
        print("Ok par iv")
        return True


def create_zip_from_file_unico(file_path, zip_file_path):
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Asegúrate de que el archivo existe
        if os.path.exists(file_path):
            # Agrega el archivo al ZIP con su nombre base
            zipf.write(file_path, os.path.basename(file_path))
        else:
            print(f"El archivo no existe: {file_path}")


def retornar_card(get_file_name, modelo, fecha, estado):  # get_fecha
    # Llama a las funciones `get_file_name` y `get_fecha` proporcionadas
    file_name = get_file_name
    # fechaHora = get_fecha()

    # Asigna el valor de `fecha_actual_render` utilizando un operador ternario
    # fecha_actual_render = str(fechaHora) if fechaHora else ""

    # Renderiza y retorna la tarjeta usando el modelo proporcionado
    return modelo.render_card(file_name, fecha, estado)

def transformar_reportes(df):
    if df.empty:
        return {}
    # Verificar la existencia de la columna
    # Lista para almacenar los valores procesados
    value_list = []

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        try:
            # Acceso seguro al valor
            variable_corte = row['Variables de corte']

            # Validar y procesar el contenido según su tipo
            if isinstance(variable_corte, list):
                # Convertir lista en un string unido por comas (si es necesario)
                processed_value = ', '.join(variable_corte)
            elif isinstance(variable_corte, str):
                # Dejar el string como está
                processed_value = variable_corte
            else:
                # Manejo de casos inesperados
                print(f"Advertencia: Tipo inesperado en la fila {index}: {type(variable_corte)}")
                continue

            # Crear el diccionario para cada entrada
            value_dict = {
                "Variables de corte": processed_value
            }

            # Agregar el diccionario a la lista
            value_list.append(value_dict)

        except Exception as e:
            print(f"Error en la fila {index}: {e}")
            continue

    return value_list

def transformar_segmentos(df):
    # Lista para almacenar los valores procesados
    value_list = []
    df.columns = df.columns.str.strip()

    # Iterar sobre las filas del DataFrame
    for index, row in df.iterrows():
        segment = row['Segment']
        rule = row['Rule']

        # Crear el diccionario para cada entrada
        value_dict = {
            "segment": segment,
            "rule": rule
        }

        # Agregar el diccionario a la lista
        value_list.append(value_dict)

    return value_list


# Transformar los datos sin cálculos adicionales
def transform_data(df):
    # Lista para almacenar los valores procesados
    value_list = []
    df.columns = df.columns.str.strip()

    print(df.columns)

    # Iterar sobre cada fila del DataFrame
    for index, row in df.iterrows():
        # Crear el diccionario para cada entrada según el formato del JSON deseado
        value_dict = {
            "Nombre Nivel": row['Nombre Nivel'],
            "Regla": f"score {row['Regla']}",
            # Convertir a string si es necesario
            "Tasa de malos máxima": (row['Tasa de Malos Máxima'])
        }

        # Agregar el diccionario a la lista
        value_list.append(value_dict)

    return value_list


id_buttons = []
id_buttons_desa = []


def crear_card_con_input(input_id, input_label, action_link_id, icon):
    id_buttons.append(action_link_id)
    return ui.column(4,
                     ui.row(
                         ui.card(
                             ui.card_header(
                                 ui.row(
                                     ui.column(10, ui.input_text(
                                         input_id, input_label)),
                                     ui.column(2,
                                               ui.input_action_link(
                                                   action_link_id, "", icon=icon, )
                                               )
                                 )
                             )
                         )
                     )
                     )


def crear_card_con_input_seleccionador(input_id, input_label, action_link_id, icon):
    # Create a card structure with a row and columns for selectize and action link
    id_buttons.append(action_link_id)
    return ui.column(4,
                     ui.card_header(
                         ui.row(
                             ui.column(
                                 10,  # Width for the selectize input
                                 ui.input_selectize(
                                     input_id,
                                     input_label,
                                     choices=[],  # Initially empty; will be updated reactively
                                     multiple=True,
                                     options={
                                         "placeholder": "seleccionar columnas..."}
                                 )
                             ),
                             ui.column(
                                 2,  # Width for the action link
                                 ui.input_action_link(
                                     action_link_id,
                                     label="",  # Can be modified to add text if needed
                                     icon=icon
                                 )
                             )
                         )
                     )

                     )


def crear_card_con_input_seleccionador_V3(input_id, input_label, action_link_id, icon):
    id_buttons_desa.append(action_link_id)
    return ui.column(4,
                     ui.card_header(
                         ui.row(
                             ui.column(
                                 10,  # Width for the selectize input
                                 ui.input_selectize(
                                     input_id,
                                     input_label,
                                     choices=[],  # Initially empty; will be updated reactively
                                     multiple=True,
                                     options={
                                         "placeholder": "seleccionar columnas..."}
                                 )
                             ),
                             ui.column(
                                 2,  # Width for the action link
                                 ui.input_action_link(
                                     action_link_id,
                                     label="",  # Can be modified to add text if needed
                                     icon=icon
                                 )
                             )
                         )
                     ),
                       
                     )


def crear_card_con_input_seleccionador_V2(input_id, input_label, action_link_id, icon):
    # Create a card structure with a row and columns for selectize and action link
    id_buttons.append(action_link_id)
    return ui.column(4,
                     ui.card_header(
                         ui.row(
                             ui.column(
                                 10,  # Width for the selectize input
                                 ui.input_selectize(
                                     input_id,
                                     input_label,
                                     choices=[],  # Initially empty; will be updated reactively
                                     multiple=True,
                                     options={
                                         "placeholder": "seleccionar columnas..."}
                                 )
                             ),
                             ui.column(
                                 2,  # Width for the action link
                                 ui.input_action_link(
                                     action_link_id,
                                     label="",  # Can be modified to add text if needed
                                     icon=icon
                                 )
                             )
                         )
                     )

                     )


def crear_card_con_input_numeric(input_id, input_label, action_link_id, icon, value=0):
    id_buttons.append(action_link_id)
    # descripcion = descripciones.get(input_id, "")
    return ui.column(4,
                     ui.row(
                             ui.card_header(
                                 ui.row(
                                     ui.column(10, ui.input_numeric(
                                         input_id, input_label, value=value)),
                                     ui.column(2,
                                               ui.input_action_link(
                                                   action_link_id, "", icon=icon)
                                               )
                                 )
                             ),
                             
                         
                     ),
                      
                     )


def crear_card_con_input_2(input_id, input_label, action_link_id, icon, parameters, default_value=""):
    id_buttons_desa.append(action_link_id)

    # Encontrar el parámetro que corresponde al input_id
    input_value = default_value
    for param in parameters:
        if param["parameter"] == input_id:
            # Si el valor es una lista, obtenemos el primer elemento
            if isinstance(param["value"], list) and len(param["value"]) > 0:
                input_value = param["value"][0].get("name", default_value)
            # Si es un valor simple, lo asignamos directamente
            else:
                input_value = param["value"]
            break

    return ui.column(4,
                     ui.row(
                         ui.card(
                             ui.card_header(
                                 ui.row(
                                     ui.column(10, ui.input_text(
                                         input_id, input_label, value=input_value)),
                                     ui.column(2,
                                               ui.input_action_link(
                                                   action_link_id, "", icon=icon)
                                               )
                                 )
                             )
                         )
                     )
                     )

def crear_card_con_input_numeric_2(input_id, input_label, action_link_id, icon, default_value,min_value=None, max_value=None, step=None):
    """
    Crea una tarjeta con un input numérico y un botón de acción.

    Args:
        input_id (str): ID del input numérico.
        input_label (str): Etiqueta del input numérico.
        action_link_id (str): ID del botón de acción.
        icon (str): Icono para el botón de acción.
        min_value (int/float, optional): Valor mínimo para el input numérico.
        max_value (int/float, optional): Valor máximo para el input numérico.
        step (int/float, optional): Paso para el input numérico.
    """
    # Añade el ID del botón de acción a la lista global (si es necesario)
    id_buttons_desa.append(action_link_id)

    # Retorna el diseño de la tarjeta con el input numérico y el botón
    return ui.column(
        4,
        ui.card_header(
            ui.row(
                ui.column(
                    10,
                    ui.input_numeric(
                        input_id,
                        input_label,
                        value=default_value,  # El valor se actualizará externamente
                        min=min_value,
                        max=max_value,
                        step=step
                    )
                ),
                ui.column(
                    2,
                    ui.input_action_link(
                        action_link_id, "", icon=icon
                    )
                )
            )
        ),
         
    )

descripciones = {
    "par_vars_segmento": "Este parámetro se utiliza para definir las variables que se mostrarán en los reportes por segmento.",
    "help_niveles": "Este parámetro muestra información sobre los niveles de riesgo.",
    "help_segmentos": "Este parámetro muestra información sobre los segmentos de mercado.",
    "help_rangos": "Este parámetro muestra información sobre los rangos de los reportes.",
    "par_times": "A mayor cantidad de replicaciones se obtiene mayor precisión pero al ser muy intensivo en CPU el método puede demorar demasiado. Se recomienda empezar con un número bajo y progresar al orden de los miles  o más si los recursos computacionales lo permiten. ",
    "par_cant_reportes": "Si se supera esta cantidad máxima se detiene la generación del cuaderno de Validación",
    "help_columnas_id": "Lista de nombres de columnas que identifcan univocamente la fila. Por ejemplo: Documento, Tipo, Sexo, Periodo.",
    "help_target_col": "Variable con valores 0 o 1.  En base a esta variable se construyen las variables Bad y Good = 1 - Bad.",
    "help_vars_forzadas": "Lista de nombres de variables que se incluyen en las candidatas aunque tengan IV muy bajo (y no sea un caso extremo)",
    "help_cols_forzadas_a_cat": "Lista de variables que se convierten a categóricas o nominales.  No hay un orden entre los distintos valores de la variable.  Deben ser disjuntas de las no predictoras. ",
    "help_iv": "Valor límite para descartar variables por bajo  Value",
    "help_cols_no_predictoras": "Lista de nombres de variables separadas por comas. Se fuerza la inclusión de las variables id y objetivo.",
    "help_limite_cor": "Se descartan las variables que luego de discretizarlas por WoE tienen una correlación de r de Pearson con la variable objetivo (ver par_target) en valor absoluto superior al valor de este parámetro. ",
    "help_minpts": "Nro. de casos mínimos de cada bin de primera etapa ",
    "help_training_testing": "El parámetro `par_split` controla como se asignan los filas para entrenamiento o validación. Admite valores no enteros entre 0 y 2. ",
    "help_par_cor_show": "Se muestran las correlaciones dentro de las variables del modelo construído que superan este límite. ",
    "help_nulos_adic": "Es una lista de nombre_var = valor nulo.  Estos valores se convierten a nulos reales. Se suman a los nulos existentes",
    "help_par_cor": "Se descartan las variables que luego de discretizarlas por WoE tienen una correlación de r de Pearson con la variable objetivo (ver par_target) en valor absoluto superior al valor de este parámetro. "

}


def create_modal_parametros(id):
    # Obtener la descripción del parámetro del diccionario
    descripcion = descripciones.get(id, "Descripción no disponible.")
    # Crear el modal
    m = ui.modal(
        "",
        # Usar el ID para el título
        title=f"Descripción del parámetro:  {descripcion}",
        body=descripcion,               # Usar la descripción en el cuerpo
        easy_close=True,
        footer=None,
    )

    return m

    # Mostrar el modal
