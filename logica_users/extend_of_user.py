from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import * 
from clases.global_session import global_session
from clases.reactives_name import global_names_reactivos
from funciones.funciones_user import button_remove, create_modal_v2
from funciones.utils_2 import leer_dataset

def extend_user_server(input: Inputs, output: Outputs, session: Session):
    
    @reactive.effect
    @reactive.event(input.files_select)  # Escuchar cambios en el selector
    def project_card_container():
        data_id = input.files_select()  # Captura el ID seleccionado
        print(data_id)
        global_session.set_id_dataSet(data_id)
        nombre_file = obtener_valor_por_id(global_session.get_id_dataSet())
        global_names_reactivos.set_name_file_db(nombre_file)
        if global_names_reactivos.get_proceso_leer_dataset():
            data = leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(), global_names_reactivos.get_name_data_Set())
            print(data)

 
    @output
    @render.ui
    def remove_dataset():
            #return button_remove(global_session.get_id_proyecto(), global_session.get_id_dataSet())
            pass
        
        
    
    @reactive.Effect
    def boton_para_eliminar_name_data_set():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_dataSet()}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
            create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_dataset", "cancelar_id_dataSet")
    
    
    @reactive.Effect
    @reactive.event(input["cancelar_id_dataSet"])
    def remove_modal_Dataset():
     ui.remove()
            
    