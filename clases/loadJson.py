
import os
import json
import traceback
from shiny import reactive
from funciones.utils_2 import get_user_directory
from clases.global_session import *

class LoadJson:
    def __init__(self ,input=None):
        self.input = input
        self.inputs = {}
        self.json = {}
        self.in_sample = reactive.value(False)
        #self.user_id = user_id

    def loop_json(self):
        try:
            self.inputs = {
                "nombre_archivo": self.inputs.get("file_desarollo"),
                "par_split": self.input["par_split"](),
                "par_ids": self.inputs.get("par_ids"),
                "par_target": self.input["par_target"](),
                "cols_forzadas_a_predictoras": self.inputs.get("cols_forzadas_a_predictoras"),
                "par_var_grupo": self.inputs.get("par_var_grupo"),
                "cols_forzadas_a_cat": self.inputs.get("cols_forzadas_a_cat"),
                "par_cor_show": self.input["par_cor_show"](),
                "par_iv": self.input["par_iv"](),
                "cols_nulos_adic":self.inputs.get("cols_nulos_adic"),
                "cols_no_predictoras":  self.inputs.get("cols_no_predictoras"),
                "par_cor": self.input["par_cor"](),
                "par_minpts1": self.input["par_minpts1"](),
                "par_discret": self.input["par_discret"](),
                "par_nbins1": self.input["par_nbins1"](),
                "par_nbins2": self.input["par_nbins2"](),
                "par_maxlevels": self.input["par_maxlevels"](),
                "par_minpts_nulos": self.input["par_minpts_nulos"](),
                "par_conf_level": self.input["par_conf_level"](),
                "par_iv_cuantiles_gb_min": self.input["par_iv_cuantiles_gb_min"](),
                "par_iv_tot_min": self.input["par_iv_tot_min"](),
                "par_iv_tot_gb_min": self.input["par_iv_tot_gb_min"](),
                "par_vars_segmento": self.inputs.get("par_vars_segmento"),
                "par_rango_niveles": self.inputs.get("par_rango_niveles", {}),
                "par_rango_segmentos": self.inputs.get("par_rango_segmentos", {}),
                "par_rango_reportes": self.inputs.get("par_rango_reportes", {}),
                "par_cant_reportes": self.input["par_cant_reportes"](),
                "par_times": self.input["par_times"](),
                "delimiter_desarollo": self.inputs.get("delimiter_desarollo"),
                "proyecto_nombre": self.inputs.get("proyecto_nombre"),
                "file_validation": self.input["file_validation"](),
                "par_minpts_cat": self.input["par_minpts_cat"](),
                "par_minpts2": self.input["par_minpts2"](),
                "par_perf_bins": self.input["par_perf_bins"](),
                "par_weight": self.inputs.get("par_weight"),

            }

            self.json = [
                {
                    "parameter": "nombre_archivo",
                    "value": self.inputs["nombre_archivo"],
                    "Descripción": "Ojo que hay cierta superposición con data_source_delim_path!",
                    "type": "list",
                },
                {
                    "parameter": "par_split",
                    "value": self.inputs["par_split"],
                    "Descripción": "",
                    "type": "numeric",
                },
                {
                    "parameter": "par_quick",
                    "value": "1",
                    "Descripción": "Cuadernos rápidos?",
                    "type": "numeric"
                },
                {
                    "parameter": "par_ids",
                    "value": self.inputs["par_ids"],
                    "Descripción": "",
                    "type": "list",
                },
                {
                    "parameter": "par_target",
                    "value": self.inputs["par_target"],
                    "Descripción": "",
                    "type": "string",
                },
                {
                    "parameter": "cols_forzadas_a_predictoras",
                    "value": self.inputs["cols_forzadas_a_predictoras"],
                    "Descripción": "Variables con inclusión forzada en las variables candidatas",
                    "type": "list"
                },
                {
                    "parameter": "par_var_grupo",
                    "value": self.inputs["par_var_grupo"],
                    "Descripción": "Variable que define grupos para evaluar las candidatas en cada uno",
                    "type": "string"
                },
                {
                    "parameter": "cols_forzadas_a_cat",
                    "value": self.inputs["cols_forzadas_a_cat"],
                    "Descripción": "Variables candidatas numéricas forzadas a categóricas",
                    "type": "list",
                },
                {
                    "parameter": "par_cor_show",
                    "value": self.inputs["par_cor_show"],
                    "Descripción": "Límite para mostrar variables por alta correlación",
                    "type": "numeric",
                },
                {
                    "parameter": "par_iv",
                    "value": self.inputs["par_iv"],
                    "Descripción": "Límite para descartar variables por bajo IV",
                    "type": "numeric",
                },
                {
                    "parameter": "cols_nulos_adic",
                    "value": self.inputs["cols_nulos_adic"],
                    "Descripción": "Lista de variables y códigos de nulos",
                    "type": "list",
                },
                {
                    "parameter": "cols_no_predictoras",
                    "value": self.inputs["cols_no_predictoras"],
                    "Descripción": "Variables excluídas de las variables candidatas",
                    "type": "list",
                },
                {
                    "parameter": "par_cor",
                    "value": self.inputs["par_cor"],
                    "Descripción": "Límite para descartar variables por alta correlación",
                    "type": "numeric",
                },
                {
                    "parameter": "par_minpts1",
                    "value": self.inputs["par_minpts1"],
                    "Descripción": "Nro. de casos mínimos de cada bin de segunda etapa",
                    "type": "numeric",
                },
                {
                    "parameter": "par_minpts2",
                    "value": self.inputs["par_minpts2"],
                    "Descripción": "Nro. de casos mínimos de cada bin de segunda etapa",
                    "type": "numeric"
                },


                {
                    "parameter": "par_discret",
                    "value": self.inputs["par_discret"],
                    "Descripción": "1 discretiza la var. continua en rampas, 0 en escalera",
                    "type": "numeric",
                },
                {
                    "parameter": "par_nbins1",
                    "value": self.inputs["par_nbins1"],
                    "Descripción": "Nro. de bines de primera etapa de la discretización monótona de variables numéricas.",
                    "type": "numeric",
                },
                {
                    "parameter": "par_nbins2",
                    "value": self.inputs["par_nbins2"],
                    "Descripción": "Nro. de bines de segunda etapa de la discretización monótona de variables numéricas.",
                    "type": "numeric",
                },
                {
                    "parameter": "par_perf_bins",
                    "value": self.inputs["par_perf_bins"],
                    "Descripción": "Nro. de \"bines\" de los reportes de performance",
                    "type": "numeric"
                },
                {
                    "parameter": "par_maxlevels",
                    "value": self.inputs["par_maxlevels"],
                    "Descripción": "Máxima cantidad de valores únicas de las variables categóricas",
                    "type": "numeric",
                },
                {
                    "parameter": "par_minpts_nulos",
                    "value": self.inputs["par_minpts_nulos"],
                    "Descripción": "Nro. de casos mínimos para asignar WoE a nulos",
                    "type": "numeric",
                },
                {
                    "parameter": "par_weight",
                    "value": self.inputs["par_weight"],
                    "type": "string"
                },
                {
                    "parameter": "par_conf_level",
                    "value": self.inputs["par_conf_level"],
                    "Descripción": "Límite para descartar variables por test de Chi-Sq en Forward",
                    "type": "numeric",
                },
                {
                    "parameter": "par_iv_cuantiles_gb_min",
                    "value": self.inputs["par_iv_cuantiles_gb_min"],
                    "Descripción": "Nro. de buenos y malos mínimos de cada cuantil para reportes de estabilidad",
                    "type": "numeric",
                },
                {
                    "parameter": "par_iv_tot_min",
                    "value": self.inputs["par_iv_tot_min"],
                    "Descripción": "Nro. de casos mínimos totales para reportes de estabilidad",
                    "type": "numeric",
                },
                {
                    "parameter": "par_iv_tot_gb_min",
                    "value": self.inputs["par_iv_tot_gb_min"],
                    "Descripción": "Nro. de buenos y malos mínimos totales para reportes de estabilidad",
                    "type": "numeric",
                },
                {
                    "parameter": "par_vars_segmento",
                    "value": self.inputs["par_vars_segmento"],
                    "Descripción": "Variables necesarias para reportes por Segmento",
                    "type": "list",
                },
                {
                    "parameter": "par_rango_niveles",
                    "Descripción": "Rango de la tabla de Niveles de Riesgo",
                    "type": "data.frame",
                    "value": self.inputs["par_rango_niveles"],
                },
                {
                    "parameter": "par_rango_segmentos",
                    "Descripción": "Rango de la tabla de Segmento",
                    "type": "data.frame",
                    "value": self.inputs["par_rango_segmentos"],
                },
                {
                    "parameter": "par_rango_reportes",
                    "Descripción": "Rango de la tabla de Reportes",
                    "type": "data.frame",
                    "value": self.inputs["par_rango_reportes"],
                },
                {
                    "parameter": "par_times",
                    "value": self.inputs["par_times"],
                    "Descripción": "Cantidad de submuestras para bootstrap",
                    "type": "numeric",
                },
                {
                    "parameter": "par_cant_reportes",
                    "value": self.inputs["par_cant_reportes"],
                    "Descripción": "Máxima cantidad de reportes",
                    "type": "numeric"
                },

                {
                    "parameter": "project_title",
                    "value": self.inputs["proyecto_nombre"],
                    "Descripción": "Título del proyecto",
                    "type": "string"

                },
                {
                    "parameter": "data_source_type",
                    "value": "DELIM",
                    "Descripción": "Tipo de la fuente de datos.",
                    "type": "string"
                },
                {
                    "parameter": "data_source_delim_path",
                    "value": "./Datos/Muestra_Desarrollo.txt",
                    "Descripción": "Ubicación del archivo de datos de desarrollo en formato plano",
                    "type": "string"
                },
                {
                    "parameter": "data_source_delim",
                    "value": self.inputs["delimiter_desarollo"],
                    "Descripción": "Tipo de la fuente de datos.",
                    "type": "string"
                },
                {
                    "parameter": "data_source_odbc_dsn",
                    "value": "BCRA",
                    "Descripción": "Nombre del DSN ODBC.",
                    "type": "string"
                },
                {
                    "parameter": "keyring_svc_odbc",
                    "value": "BCRA",
                    "Descripción": "Nombre del servicio en keyring por defecto",
                    "type": "string"
                },
                {
                    "parameter": "data_source_query",
                    "value": "SELECT variables FROM [esquema].[dbo].[tabla]",
                    "Descripción": "Query proveedor de datos para desarrollo",
                    "type": "string"
                },
                {
                    "parameter": "par_minpts_cat",
                    "value": self.inputs["par_minpts_cat"],
                    "Descripción": "Nro. de casos mínimos de cada bin de la discretización de categorícas",
                    "type": "numeric"
                },
                {
                    "parameter": "data_source_val_delim_path",
                    "value": "./Datos/Muestra_Validación.txt",
                    "Descripción": "Ubicación del archivo de datos de validación en formato plano",
                    "type": "string"
                },
                {
                    "parameter": "data_source_scoring_delim_path",
                    "value":"./Datos/Muestra_Scoring.txt",
                    "Descripción": "Ubicación del archivo de datos para scoring en formato plano",
                    "type": "string"
                }



            ]
        except KeyError as e:
            print(f"Error: Clave no encontrada en los inputs: {str(e)}")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {str(e)}")
            traceback.print_exc()
        # Crear la lista de diccionarios en el formato deseado
        #get_user_directory(self.user_id)
        directorio_guardado = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        #ruta_json = os.path.join(directorio_guardado, 'Control_de_SmartModelStudio.json')

        #C:\Users\fvillanueva\Desktop\SmartModel_new_version\new_version_new\Automat\datos_entrada_auth0_670fc1b2ead82aaae5c1e9ba\proyecto_62_test now\version__Version ver
        ruta_json = os.path.join(
            directorio_guardado, 'Control de SmartModelStudio.json')
        with open(ruta_json, 'w', encoding='utf-8') as file:
            json.dump(self.json, file, ensure_ascii=False, indent=4)

        return ruta_json

    def load_json(self):
        directorio_guardado = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}'
        ruta_json = os.path.join(directorio_guardado, 'Control de SmartModelStudio.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as file:
                self.inputs = json.load(file)
                # print("Valores cargados:", self.inputs)
                return self.inputs
            

    def update_values(self, updates):
        """
        Actualiza el JSON cargado con los valores proporcionados en un diccionario.
        :param updates: Diccionario donde las claves son los nombres de los parámetros ('parameter')
                        y los valores son los nuevos valores ('value').
        :return: Lista de diccionarios actualizada.
        """
        # Cargar los valores actuales del JSON
        valores = self.load_json()
        if not valores:
            print("No se encontraron valores para actualizar. JSON vacío o no cargado.")
            return []

        # Recorrer las actualizaciones y aplicar los cambios
        for update_key, update_value in updates.items():
            actualizado = False
            for item in valores:
                # Si el parámetro existe, actualizamos su valor
                if item.get('parameter') == update_key:
                    print(f"Actualizando {update_key}: {item['value']} -> {update_value}")
                    item['value'] = update_value
                    break

        # Guardar los cambios en self.inputs y devolver los valores actualizados
        self.inputs = valores
        return valores
                

    def save_json(self):
        directorio_guardado = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}'
        ruta_json = os.path.join(directorio_guardado, 'Control de SmartModelStudio.json')

        os.makedirs(directorio_guardado, exist_ok=True)  # Asegurarse de que exista el directorio
        with open(ruta_json, 'w', encoding='utf-8') as file:
            json.dump(self.inputs, file, ensure_ascii=False, indent=4)



#global_json = LoadJson()
