from shiny import App, ui, reactive
from clases.loadJson import LoadJson
from funciones.create_param import create_screen
from clases.class_user_proyectName import global_user_proyecto
from funciones.utils import crear_card_con_input_seleccionador_V2, crear_card_con_input_numeric_2, crear_card_con_input_seleccionador
from global_names import global_name_desarrollo
from clases.global_session import global_session
from global_var import global_data_loader_manager

user_id = global_session.obtener_id()
json_loader = LoadJson(user_id=user_id)
previous_values = json_loader.load_json()
nombre_proyecto = global_user_proyecto

name_suffix = "desarrollo"
CHOICES = {
    "tipo": [",", '\\t', "' '", ";", "|"],
}

data_loader = global_data_loader_manager.get_loader(name_suffix)

# Página principal de desarrollo
screenDesarollo = ui.page_fluid(
    # Selección de columnas de dataset
    
    ui.div(
        ui.tags.div(
            ui.card(
                    ui.output_ui("devolver_acordeon"),
                ),
            
            
        id="module_container",
    ),
        ui.tags.div(ui.column(12, ui.input_select(
            "number_choice",
            "Selecciona un número de columnas de dataset",
            choices=[str(i) for i in range(5, 26)],
            width="30%"
        ))),
        
        ui.output_text_verbatim("error"),
        ui.output_text_verbatim("error_proyecto"),
        ui.div(
            ui.card(
                ui.card_header(f"Datos de {name_suffix}"),
                ui.output_data_frame(f"summary_data_{name_suffix}"),
            ),
        ),
        ui.h3(f"Parámetros de {name_suffix}", fillable=True),
    ),
    
    ui.tags.hr(),  # Separador

    
    
    ui.tags.hr(),  # Separador
    
    # Estado del archivo y contenido de pantalla
    ui.row(
        ui.column(12, ui.output_text_verbatim("file_status_desarollo")),
        ui.output_ui("update_action_button"),
        ui.output_ui("screen_content_desarollo"),
    ),
    
    ui.div(class_="mt-5"),  # Espaciador
    
    ui.output_ui("parametros_desarrolo"),
    
    # Navegación con pestañas
    ui.navset_card_underline(
        # Pestaña de Ejecución
        ui.nav_panel(
            "Ejecución",
                    ui.output_ui("card_desarollo2"),
                    ui.output_ui("tarjeta_desarollo"),
                    ui.output_ui("mensaje_desarollo"),
                    ui.output_text_verbatim("mostrarDatos"),
                    ui.output_ui("boton_desarollo"),
                    ui.output_ui("descarga_desarollo"),
                    value="desarrollo"
                ),

        ui.nav_spacer(),
        
        #ui.nav_control(ui.input_task_button(f"start_{name_suffix}", f"Comenzar proyecto")),  
        # Pestaña de Resultados
        ui.nav_panel(
            "Resultados",
            ui.div(
                ui.card(
                    "Resultados de desarrollo",
                    ui.column(4, ui.download_button(
                        "descargar_resultados_desarollo", "Descargar Todos los reportes desarrollo")),
                    ui.output_ui("render_resultado_card"),
                    ui.output_ui("funcion_volver"),
                    #ui.output_ui("render_desarollo_resultado_dos"),
                    #ui.output_ui("resultado_card_clean_trans"),
                    #ui.output_ui("resultado_card_desarollo4"),
                    #ui.output_ui("html_output_desarollo2"),
                    #ui.output_ui("html_output_desarollo3"),
                    value="desarrollo"
                )
            ),
        ),
    ),
)
