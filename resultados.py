from shiny import reactive, render, ui
from clases.class_result import ResultadoClass
from clases.class_resultado import ResultadoClassPrueba
from clases.global_session import global_session
from funciones.create_menu_resul_model import create_nav_menu_result_model
from clases.class_user_proyectName import global_user_proyecto


def server_resul(input, output, session, name_suffix):
    proceso_ok = reactive.Value(False)
    user_id_global = None

    @output
    @render.text
    def nombre_proyecto_resultados():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo()}'

    @output
    @render.ui
    def menu_resultados():
        return create_nav_menu_result_model(name_suffix)

   

    def get_user_id_from_session():
        @reactive.effect
        def enviar_session():
            if global_session.proceso.get():
                state = global_session.session_state.get()
                if state["is_logged_in"]:
                    user_id = state["id"].replace('|', '_')
                    global user_id_global
                    user_id_global = user_id
                    print(f"[get_user_id_from_session] user_id_global asignado: {user_id_global}")
                    return user_id
                
    get_user_id_from_session()
    def crear_resultados_desarrollo():
        resultados_desarrollo = [
            {
                "resultado_id": "Clean_Transf",
                "resultado_path": f"mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes/Clean-Transf.html",
                "salida": "result_Clean_Transf",
                "salida_unic": "salida_prueba_Clean_Transf",
                "descarga_unic": "download_btn1_Clean_Transf",
            },
            {
                "resultado_id": "Detalle_agrupacion",
                "resultado_path": f"mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes/Detalle agrupación x WoE Categoricas.html",
                "salida": "Detalle_agrupación_salida",
                "descarga_unic": "download_btn_Detalle_agrupacion",
                "salida_unic": "salida_prueba_Detalle_agrupación",
            },
            {
                "resultado_id": "Detalle_agrupación_continuas",
                "resultado_path": f"mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes/Detalle agrupación x WoE Continuas (Monotonía más Interpolación Lineal a Trozos).html",
                "salida": "download_btn_Detalle_agrupacionContinuas",
                "descarga_unic": "download_btn_Detalle_agrupacion_continuas",
                "salida_unic": "salida_prueba_Detalle_agrupación_continuas",
            },
            {
                "resultado_id": "detalle_monotonia",
                "resultado_path": f"mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes/Detalle agrupación x WoE Continuas (Monotonía).html",
                "salida": "detalle_monotonia_salida",
                "descarga_unic": "download_btn_detalle_monotonia",
                "salida_unic": "salida_detalle_monotonia",
            },
            {
                "resultado_id": "modelling",
                "resultado_path": f"mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id_global}/Reportes/Modelling.html",
                "salida": "detalle_modelling",
                "descarga_unic": "download_btn_modelling",
                "salida_unic": "salida_modelling",
            },
        ]
        return resultados_desarrollo
    
    resultados_desarrollo = crear_resultados_desarrollo()


    resultados_in_sample = [
        {
            "resultado_id": "Validation_InS",
            "resultado_path": r"/mnt/c/Users/fvillanueva/flask_prueba/static/Validation_InS.html",
            "salida": "result_in_sample_salida",
            "salida_unic": "salida_prueba_in_sample",
            "descarga_unic": "download_btn1_insample",
        },
    ]

    resultados_out_to_sample = [
        {
            "resultado_id": "Resultados_Oss",
            "resultado_path": r"/mnt/c/Users/fvillanueva/flask_prueba/static/Validation_OoS.html",
            "salida": "output_modelling_out",
            "salida_unic": "salida_prueba_out_to",
            "descarga_unic": "download_btn1",
        },
    ]

    resultados_produccion = [
        {
            "resultado_id": "Scoring",
            "resultado_path": r"/mnt/c/Users/fvillanueva/flask_prueba/static/Scoring.html",
            "salida": "output_modelling",
            "salida_unic": "salida_prueba",
            "descarga_unic": "download_produccion_scoring",
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
            return salida_in_sample_unic

    def create_dynamic_output(resultado_id, salida):
        # print("salidas", salida)
        @output(id=salida)
        @render.ui
        def dynamic_output():
            html_desarrollo = resultado_desarrollo.html_output_prueba(resultado_id)
            html_prueba = resultado_class_instance.html_output_prueba(resultado_id)
            html_produccion = resultado_class_instance_produccion.html_output_prueba(resultado_id)
            html_in_sample = resultado_in_sample.html_output_prueba(resultado_id)
            return html_prueba, html_produccion, html_in_sample, html_desarrollo

    def descargas_dinamicas(resultado_id, descarga_unic,filename):
        @output(id=descarga_unic)
        @render.download(filename=filename)
        def download_btn1_():
            salida_desarrollo = resultado_desarrollo.descargar_unico_html(resultado_id)
            salida_ot_sample = resultado_class_instance_produccion.descargar_unico_html(resultado_id)
            salida_in_sample = resultado_in_sample.descargar_unico_html(resultado_id)
            salida_produccion = resultado_class_instance_produccion.descargar_unico_html(resultado_id)
            return salida_in_sample, salida_ot_sample, salida_produccion, salida_desarrollo

        return download_btn1_

    def register_outputs(resultados):
        for r in resultados:
            resultado_id = r['resultado_id']
            salida = r['salida']
            descarga_unic = r['descarga_unic']
            salida_unic = r['salida_unic']
            filename = f"{resultado_id}.zip"
            # print("Procesando resultado_id: ", resultado_id)

            # Crear el output dinámico
            create_dynamic_output(resultado_id, salida)

            create_salida_unic(resultado_id, salida_unic)

            descargas_dinamicas(resultado_id, descarga_unic,filename)

    # Invocar la función para registrar los outputs
    combined_results = resultados_produccion + resultados_out_to_sample + resultados_in_sample + resultados_desarrollo
    register_outputs(combined_results)

    # Definir el output principal
    @output
    @render.ui
    def render_resultado_card():
        resultado_desarrollo.abrir_acordeon(input)
        return resultado_desarrollo.resultado_cards()

    
    @output
    @render.ui
    def resultado_card_validacion_in_sample():
        resultado_in_sample.abrir_acordeon(input)
        return resultado_in_sample.resultado_cards()

    @output
    @render.ui
    def resultado_card_validacion_out_to_sample():
        resultado_class_instance.abrir_acordeon(input)
        return resultado_class_instance.resultado_cards()

    @output
    @render.ui
    def resultado_card_produccion():
        resultado_class_instance_produccion.abrir_acordeon(input)
        return resultado_class_instance_produccion.resultado_cards()

    # register_outputs(resultados_produccion)

    @output
    @render.ui
    def resultado_card_produccion():
        resultado_class_instance_produccion.abrir_acordeon(input)
        return resultado_class_instance_produccion.resultado_cards()
    
    
    @output
    @render.download(filename="Clean_Transf.zip")
    def download_btn1_Clean_Transf():
        resultado_id  = "Clean_Transf"
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Detalle_agrupacion.zip")
    def download_btn_Detalle_agrupacion():
        resultado_id  = "Detalle_agrupacion"
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Detalle_agrupacion_continuas.zip")
    def download_btn_Detalle_agrupacion_continuas():
        resultado_id  = "Detalle_agrupacion_continuas"
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="detalle_monotonia.zip")
    def download_btn_detalle_monotonia():
        resultado_id  = "detalle_monotonia"
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="modelling.zip")
    def download_btn_modelling():
        resultado_id  = "modelling"
        return resultado_desarrollo.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Validation_InS.zip")
    def download_btn1_insample():
        resultado_id  = "Validation_InS"
        return resultado_in_sample.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Resultados_Oss.zip")
    def download_btn1():
        resultado_id  = "Resultados_Oss"
        return resultados_out_to_sample.descargar_unico_html(resultado_id)
    
    @output
    @render.download(filename="Scoring.zip")
    def download_produccion_scoring():
        resultado_id  = "Scoring"
        return resultado_class_instance_produccion.descargar_unico_html(resultado_id)
    
        
    
    @render.download(filename="Resultados completos de desarollo.zip")
    def descargar_resultados_desarollo():
        return resultado_desarrollo.descargar_resultados()
    
    @render.download(filename="Resultados completos de In-Sample.zip")
    def descargar_resultados_validacion():
        return resultado_in_sample.descargar_resultados()
    
    @render.download(filename="Resultados completos de Out-of-Sample.zip")
    def descargar_resultados_validacion_out_of_sample():
        return resultados_out_to_sample.descargar_resultados()
    
    @render.download(filename="Resultados completos de Producción.zip")
    def descargar_resultados_produccion():
        return resultado_class_instance_produccion.descargar_resultados()

    
    
    
    
    
    
    
    
    
    
    
    

    def create_navigation_handler(input_id, screen_name):
        @reactive.Effect
        @reactive.event(input[input_id])
        async def navigate():
            await session.send_custom_message('navigate', screen_name)
    # NAVEGACIONES DE MENU
    create_navigation_handler('start_resultados', 'Screen_User')
    create_navigation_handler(
        'screen_in_sample_resultados', 'screen_in_sample')
    create_navigation_handler(
        'screen_Desarollo_resultados', 'Screen_Desarollo')
    create_navigation_handler('load_Validacion_resultados', 'Screen_valid')
    create_navigation_handler(
        'screen_Produccion_resultados', 'Screen_Porduccion')
    create_navigation_handler("ir_modelos_resultados", "Screen_3")
    create_navigation_handler("ir_result_resultados", "Screen_Resultados")
    create_navigation_handler("volver_resultados", "Screen_User")
