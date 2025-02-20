from shiny import reactive, render, ui
from clases.class_result import ResultadoClass
from clases.class_resultado import ResultadoClassPrueba
from clases.global_session import global_session
from funciones.create_menu_resul_model import create_nav_menu_result_model
from clases.class_user_proyectName import global_user_proyecto
from api.db import *
import os
from clases.global_sessionV2 import *
from servers.utils.get_paths import get_output_path


def server_resul(input, output, session, name_suffix):

    @output
    @render.text
    def nombre_proyecto_resultados():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo(global_session.proyecto_seleccionado())}'

    @output
    @render.ui
    def menu_resultados():
        return create_nav_menu_result_model(name_suffix)

   

    def get_user_id_from_session():
        @reactive.effect
        def enviar_session():
            state = global_session.session_state.get()
            if state["is_logged_in"]:
                user_id = state["id"].replace('|', '_')
                global user_id_global
                user_id_global = user_id
                print(f"[get_user_id_from_session] user_id_global asignado: {user_id_global}")
                return user_id
            
    user_id = get_user_id_from_session()
   
   
    def crear_resultados_desarrollo():
        resultados_desarrollo = [
            {
                "resultado_id": "Clean_Transf",
                "resultado_path": f"Clean-Transf.html",
                "salida": "result_Clean_Transf",
                "salida_unic": "salida_prueba_Clean_Transf",
                "descarga_unic": "download_btn1_Clean_Transf",
            },
            {
                "resultado_id": "Detalle_agrupacion",
                "resultado_path": f"WoE Discretization on Categorical.html",
                "salida": "Detalle_agrupación_salida",
                "descarga_unic": "download_btn_Detalle_agrupacion",
                "salida_unic": "salida_prueba_Detalle_agrupación",
            },
            {
                "resultado_id": "Detalle_agrupación_continuas",
                "resultado_path": f"WoE PWL discretization on Continuous.html",
                "salida": "download_btn_Detalle_agrupacionContinuas",
                "descarga_unic": "download_btn_Detalle_agrupacion_continuas",
                "salida_unic": "salida_prueba_Detalle_agrupación_continuas",
            },
            {
                "resultado_id": "detalle_monotonia",
                "resultado_path": f"WoE Discretization on Categorical.html",
                "salida": "detalle_monotonia_salida",
                "descarga_unic": "download_btn_detalle_monotonia",
                "salida_unic": "salida_detalle_monotonia",
            },
            {
                "resultado_id": "modelling",
                "resultado_path": f"Modelling_quick.html",
                "salida": "detalle_modelling",
                "descarga_unic": "download_btn_modelling",
                "salida_unic": "salida_modelling",
            },
        ]
        return resultados_desarrollo
    
    resultados_desarrollo = crear_resultados_desarrollo()

    def resultados_niveles_Scorcards():
        resultados_in_sample = [
            {
                "resultado_id": "Validation_InS",
                "resultado_path": f"Validation_InS.html",
                "salida": "result_in_sample_salida",
                "descarga_unic": "download_btn1_insample",
                "salida_unic": "salida_prueba_in_sample",
                
            },
        ]
        return resultados_in_sample

    resultados_in_sample = resultados_niveles_Scorcards()
    
    resultados_out_to_sample = [
        {
            "resultado_id": "Resultados_Oss",
            "resultado_path": "Validation_OoS.html",
            "salida": "output_modelling_out",
            "descarga_unic": "download_btn1_sample",
            "salida_unic": "salida_prueba_out_to",
        },
    ]

    resultados_produccion = [
        {
            "resultado_id": "Scoring",
            "resultado_path": "Scoring.html",
            "salida": "output_modelling",
            "descarga_unic": "download_produccion_scoring",
            "salida_unic": "salida_prueba",
        },
        
    ]
    resultado_desarrollo = ResultadoClassPrueba(resultados_desarrollo)
    resultado_class_instance = ResultadoClassPrueba(resultados_out_to_sample)
    resultado_in_sample = ResultadoClassPrueba(resultados_in_sample)
    resultado_class_instance_produccion = ResultadoClassPrueba(resultados_produccion)
    
    

    def create_salida_unic(resultado_id, salida_unic):
        @output(id=salida_unic)
        @render.ui
        def dynamic_salida_unic():
            salida_in_sample_unic = resultado_in_sample.boton_para_descagar_unico(
                resultado_id)
            #return salida_in_sample_unic

    def create_dynamic_output(resultado_id, salida):
        # print("salidas", salida)
        @output(id=salida)
        @render.ui
        def dynamic_output():
            html_desarrollo = resultado_desarrollo.html_output_prueba(resultado_id)
            html_prueba = resultado_class_instance.html_output_validacion_scoring(resultado_id)
            html_produccion = resultado_class_instance_produccion.html_output_validacion_scoring(resultado_id)
            html_in_sample = resultado_in_sample.html_output_in_sample(resultado_id)
            return html_prueba, html_produccion, html_in_sample, html_desarrollo


   
        #return download_btn1_

    def register_outputs(resultados):
        for r in resultados:
            resultado_id = r['resultado_id']
            salida = r['salida']
            descarga_unic = r['descarga_unic']
            salida_unic = r['salida_unic']
            filename = f"{resultado_id}.zip"
            # print("Procesando resultado_id: ", resultado_id)

            # Crear el output dinámico
            print(resultado_id, "id a regitrar?x")
            create_dynamic_output(resultado_id, salida)

            create_salida_unic(resultado_id, salida_unic)

            #descargas_dinamicas(resultado_id, descarga_unic,filename)

    # Invocar la función para registrar los outputs
    combined_results = resultados_produccion + resultados_out_to_sample + resultados_in_sample + resultados_desarrollo
    register_outputs(combined_results)
    
    
    
    

    # Definir el output principal
    @output
    @render.ui
    def render_resultado_card():
        resultado_desarrollo.abrir_acordeon(input)
        resultado_desarrollo.obtener_user_id()
        return resultado_desarrollo.resultado_cards()

    
    @output
    @render.ui
    def resultado_card_validacion_in_sample():
        resultado_in_sample.abrir_acordeon(input)
        resultado_in_sample.obtener_user_id()
        return resultado_in_sample.resultado_cards()

    @output
    @render.ui
    def resultado_card_validacion_out_to_sample():
        resultado_class_instance.abrir_acordeon(input)
        resultado_class_instance.obtener_user_id()
        return resultado_class_instance.resultado_cards()

    @output
    @render.ui
    def resultado_card_produccion():
        resultado_class_instance_produccion.abrir_acordeon(input)
        resultado_class_instance_produccion.obtener_user_id()
        return resultado_class_instance_produccion.resultado_cards()

    # register_outputs(resultados_produccion)

    @output
    @render.ui
    def resultado_card_produccion():
        resultado_class_instance_produccion.abrir_acordeon(input)
        resultado_class_instance_produccion.obtener_user_id()
        return resultado_class_instance_produccion.resultado_cards()
    
    
    @output
    @render.download(filename="Clean_Transf.zip")
    def download_btn1_Clean_Transf():
        resultado_id  = "Clean_Transf"
        resultado_desarrollo.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="desarrollo")
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Detalle_agrupacion.zip")
    def download_btn_Detalle_agrupacion():
        resultado_id  = "Detalle_agrupacion"
        resultado_desarrollo.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="desarrollo")
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Detalle_agrupacion_continuas.zip")
    def download_btn_Detalle_agrupacion_continuas():
        resultado_id  = "Detalle_agrupacion_continuas"
        resultado_desarrollo.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="desarrollo")
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="detalle_monotonia.zip")
    def download_btn_detalle_monotonia():
        resultado_id  = "detalle_monotonia"
        resultado_desarrollo.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="desarrollo")
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="modelling.zip")
    def download_btn_modelling():
        resultado_id  = "modelling"
        resultado_desarrollo.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="desarrollo")
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Validation_InS.zip")
    def download_btn1_insample():
        resultado_id  = "Validation_InS"
        insample_path = get_output_path(resultado_id, global_session, global_session_V2, modo="in_sample")
        return resultado_class_instance.descargar_resultados(insample_path)
    
    @output
    @render.download(filename="Resultados_Oss.zip")
    def download_btn1_sample(): 
        resultado_id  = "Resultados_Oss"
        path_of_sample_resultados =  get_output_path(resultado_id, global_session, global_session_V2, modo="full")
        return resultado_class_instance.descargar_resultados(path_of_sample_resultados)
    
    
    @output
    @render.download(filename="Scoring.zip")
    def download_produccion_scoring():
        resultado_id  = "Scoring"
        resultado_class_instance_produccion.path_resultados = get_output_path(resultado_id, global_session, global_session_V2, modo="scoring")
        return resultado_class_instance_produccion.descargar_unico_html(resultado_id)
    
        
    
    @render.download(filename="Resultados completos de desarrollo.zip")
    def descargar_resultados_desarollo():
        file_path = f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/Reportes"              
        return resultado_desarrollo.descargar_resultados(file_path)
    
    @render.download(filename="Resultados completos de Niveles & scorecards.zip")
    def descargar_resultados_validacion():
        path_in_sample_resultados =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/Reportes'         
        return resultado_in_sample.descargar_resultados(path_in_sample_resultados)
    
    @render.download(filename="Resultados completos de Out-of-Sample.zip")
    def descargar_resultados_validacion_out_to_sample():
        path_of_sample_resultados =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/{global_session_V2.nombre_file_sin_extension_validacion_scoring.get()}/Reportes'
        return resultado_class_instance.descargar_resultados(path_of_sample_resultados)
    
    @render.download(filename="Resultados completos de Producción.zip")
    def descargar_resultados_produccion():
        salida =  f'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{global_session.get_id_user()}/proyecto_{global_session.get_id_proyecto()}_{global_session.get_name_proyecto()}/version_{global_session.get_id_version()}_{global_session.get_versiones_name()}/version_parametros_{global_session.get_version_parametros_id()}_{global_session.get_versiones_parametros_nombre()}/{global_session_V2.nombre_file_sin_extension_validacion_scoring.get()}/Reportes'
        return resultado_class_instance_produccion.descargar_resultados(salida)