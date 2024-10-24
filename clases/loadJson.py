
import os
import json
import traceback
from shiny import reactive
from funciones.utils_2 import get_user_directory

class LoadJson:
    def __init__(self, user_id ,input=None):
        self.input = input
        self.inputs = {}
        self.json = {}
        self.user_id = user_id

    def loop_json(self):
        try:
            self.inputs = {
                "nombre_archivo": self.input["file_desarollo"](),
                "par_split": self.input["par_split"](),
                "par_ids": self.inputs.get("par_ids"),
                "par_target": self.inputs.get("par_target"),
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
                "par_limit_by_minbinq": self.input["par_limit_by_minbinq"](),
                "par_limit_by_minbinw": self.input["par_limit_by_minbinw"](),
                "par_iv_cuantiles_gb_min": self.input["par_iv_cuantiles_gb_min"](),
                "par_iv_tot_min": self.input["par_iv_tot_min"](),
                "par_iv_tot_gb_min": self.input["par_iv_tot_gb_min"](),
                "par_vars_segmento": self.inputs.get("par_vars_segmento"),
                "par_rango_niveles": self.inputs.get("par_rango_niveles", {}),
                "par_rango_segmentos": self.inputs.get("par_rango_segmentos", {}),
                "par_rango_reportes": self.inputs.get("par_rango_reportes", {}),
                "par_times": self.input["par_times"](),
                "par_cant_reportes": self.input["par_cant_reportes"](),
                "delimiter_desarollo": self.input["delimiter_desarollo"](),
                "proyecto_nombre": self.input["proyecto_nombre"](),
                "file_validation": self.input["file_validation"](),
                "file_produccion": self.input["file_produccion"](),
                "par_minpts_cat": self.input["par_minpts_cat"](),
                "par_minpts2": self.input["par_minpts2"](),
                "par_perf_bins": self.input["par_perf_bins"](),
                "par_weight": self.input["par_weight"]()

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
                    "type": "string"
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
                    "type": "string",
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
                    "type": "string",
                },
                {
                    "parameter": "cols_no_predictoras",
                    "value": self.inputs["cols_no_predictoras"],
                    "Descripción": "Variables excluídas de las variables candidatas",
                    "type": "string",
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
                    "parameter": "par_limit_by_minbinq",
                    "value": self.inputs["par_limit_by_minbinq"],
                    "Descripción": "Medir el tamaño de los bines según su cantidad de casos",
                    "type": "numeric",
                },
                {
                    "parameter": "par_weight",
                    "value": self.inputs["par_weight"],
                    "type": "string"
                },
                {
                    "parameter": "par_limit_by_minbinw",
                    "value": self.inputs["par_limit_by_minbinw"],
                    "Descripción": "Medir el tamaño de los bines según su peso dado par_weight",
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
                    "type": "string",
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
                    "value": self.inputs["file_validation"],
                    "Descripción": "Ubicación del archivo de datos de validación en formato plano",
                    "type": "string"
                },
                {
                    "parameter": "data_source_scoring_delim_path",
                    "value": self.inputs["file_produccion"],
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
        directorio_guardado = f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada_{self.user_id}'
        ruta_json = os.path.join(
            directorio_guardado, 'Control de SmartModelStudio.json')
        with open(ruta_json, 'w', encoding='utf-8') as file:
            json.dump(self.json, file, ensure_ascii=False, indent=4)

        return ruta_json

    def load_json(self):
        directorio_guardado = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_entrada'
        ruta_json = os.path.join(directorio_guardado, 'Control de SmartModelStudio.json')
        if os.path.exists(ruta_json):
            with open(ruta_json, 'r', encoding='utf-8') as file:
                self.inputs = json.load(file)
                # print("Valores cargados:", self.inputs)
                return self.inputs

    def get_json_value(self, parameter, default_value=None):
        for item in self.inputs:  # Assuming self.inputs is the loaded JSON data
            if isinstance(item, dict) and item.get('parameter') == parameter:
                return item.get('value', default_value)
        return default_value


#global_json = LoadJson()
