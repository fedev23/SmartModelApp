from shiny import reactive, render, ui
from clases.class_result import ResultadoClass
from clases.class_resultado import ResultadoClassPrueba

from funciones.create_menu_resul_model import create_nav_menu_result_model
from clases.class_user_proyectName import global_user_proyecto


def server_resul(input, output, session, name_suffix):
    proceso_ok = reactive.Value(False)

    @output
    @render.text
    def nombre_proyecto_resultados():
        return f'Proyecto: {global_user_proyecto.mostrar_nombre_proyecto_como_titulo()}'

    @output
    @render.ui
    def menu_resultados():
        return create_nav_menu_result_model(name_suffix)

   

    # Descargar todos los resultados de desarollo
    @render.download(filename="Resultados completos de desarollo.zip")
    def descargar_resultados_desarollo():
        return resultado_desarrollo.descargar_resultados()

    resultados_desarrollo = [
        {
            "resultado_id": "Clean_Transf",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Clean-Transf.html",
            "salida": "result_Clean_Transf",
            "salida_unic": "salida_prueba_Clean_Transf",
            "descarga_unic": "download_btn1_Clean-Transf",
        },
        {
            "resultado_id": "Detalle_agrupación",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Detalle agrupación x WoE Categoricas.html",
            "salida": "Detalle_agrupación_salida",
            "descarga_unic": "download_btn_Detalle_agrupación",
            "salida_unic": "salida_prueba_Detalle_agrupación",
        },
        {
            "resultado_id": "Detalle_agrupación_continuas",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Detalle agrupación x WoE Continuas  (Monotonía más Interpolación Lineal a Trozos).html",
            "salida": "Detalle_agrupación_continuas_salida",
            "descarga_unic": "download_btn_Detalle_agrupación_continuas",
            "salida_unic": "salida_prueba_Detalle_agrupación_continuas",
        },
        {
            "resultado_id": "detalle_monotonia",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Detalle agrupación x WoE Continuas  (Monotonía).html",
            "salida": "detalle_monotonia_salida",
            "descarga_unic": "download_btn_detalle_monotonia",
            "salida_unic": "salida_detalle_monotonia",
        },
        {
            "resultado_id": "modelling",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Modelling.html",
            "salida": "detalle_modelling",
            "descarga_unic": "download_btn_modelling",
            "salida_unic": "salida_modelling",
        },

    ]

    resultados_in_sample = [
        {
            "resultado_id": "result_in_sample",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Validation_InS.html",
            "salida": "result_in_sample_salida",
            "salida_unic": "salida_prueba_in_sample",
            "descarga_unic": "download_btn1_insample",
        },
        {
            "resultado_id": "Modelling_sample",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Modelling.html",
            "salida": "meddling_in_sample",
            "descarga_unic": "download_btn_wo",
            "salida_unic": "salida_prueba_in_sample_1",
        },

    ]

    resultados_out_to_sample = [
        {
            "resultado_id": "Modelling_v1",
            "resultado_path": r"C:\Users\fvillanueva\Desktop\SmartModel_new_version\datos_salida\Reportes\Modelling_v10.html",
            "salida": "output_modelling_out",
            "salida_unic": "salida_prueba_out_to",
            "descarga_unic": "download_btn1",
        },
        {
            "resultado_id": "Modelling_v10002",
            "resultado_path": r"C:\Users\fvillanueva\Desktop\SmartModel_new_version\datos_salida\Reportes\Detalle agrupación x WoE Continuas  (Monotonía).html",
            "salida": "output_woe_out_to",
            "descarga_unic": "download_btn_woe_in_sample",
            "salida_unic": "salida_prueba1",
        },
        {
            "resultado_id": "resultado3",
            "resultado_path": r"C:\Users\fvillanueva\Desktop\SmartModel_new_version\datos_salida\Reportes\Detalle agrupación x WoE Continuas  (Monotonía).html",
            "salida": "output_3",
            "descarga_unic": "download_btn_3",
            "salida_unic": "salida_prueba2",
        },
        {
            "resultado_id": "Modelling_4",
            "resultado_path": r"C:\Users\fvillanueva\Desktop\SmartModel_new_version\datos_salida\Reportes\Detalle agrupación x WoE Continuas  (Monotonía).html",
            "salida": "output_4",
            "descarga_unic": "download_btn_4",
            "salida_unic": "salida_prueba3",
        },

    ]

    resultados_produccion = [
        {
            "resultado_id": "Scorin",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Scoring.html",
            "salida": "output_modelling",
            "salida_unic": "salida_prueba",
            "descarga_unic": "download_produccion_scoring",
        },
        {
            "resultado_id": "Modelling_produccion",
            "resultado_path": r"C:\Users\fvillanueva\flask_prueba\static\Modelling.html",
            "salida": "output_woe_produccion",
            "descarga_unic": "download_btn_produccion",
            "salida_unic": "salida_prueba_produccion",
        }

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

    def descargas_dinamicas(resultado_id, filename):
        @output(id=resultado_id)
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

            descargas_dinamicas(resultado_id, filename)

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
