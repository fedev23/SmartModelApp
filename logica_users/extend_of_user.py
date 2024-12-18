from shiny import App, Inputs, Outputs, Session, reactive, ui, render, module
from funciones.nav_panel_User import create_nav_menu_user
from clases.class_user_proyectName import global_user_proyecto
from api import * 
from clases.global_session import global_session
from clases.reactives_name import global_names_reactivos
from funciones.funciones_user import button_remove, create_modal_v2
from funciones.utils_2 import leer_dataset
from logica_users.utils.help_versios import obtener_ultimo_nombre_archivo
from funciones.clase_estitca.leer_datos import DatasetHandler
from clases.global_sessionV2 import *
from clases.global_reactives import global_estados
from api.db.sqlite_utils import *


def extend_user_server(input: Inputs, output: Outputs, session: Session, name):
    
    dataSet_predeterminado_parms = reactive.Value(None)
    list = reactive.Value(None)
    id = reactive.Value(None)
    select_number_data_set =  reactive.Value(5)
    
    @reactive.effect
    @reactive.event(input.files_select)  # Escuchar cambios en el selector
    def project_card_container():
        data_id = input.files_select()  # Captura el ID seleccionado
        global_session.set_id_dataSet(data_id)
        
        base_datos = 'Modeling_App.db'
        tabla = 'name_files'
        columna_objetivo = 'nombre_archivo'
        columna_filtro = 'id_files'
        nombre_file = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session.get_id_dataSet())
        
        actualizar_ultimo_seleccionado(base_datos, 'name_files', 'id_files', data_id)
        ##OBTENGO LOS VALORES ASOCIADOS A LA TABALA
        list = get_records(table='name_files',
            columns=['name_files.id_files', 'name_files.nombre_archivo', 'name_files.fecha_de_carga'],
            join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),))
        
        
        global_names_reactivos.set_name_file_db(nombre_file)
        
        if global_names_reactivos.get_name_file_db() is None:
            global_session_V2.set_dataSet_seleccionado(obtener_ultimo_nombre_archivo(list))
        else:
            global_session_V2.set_dataSet_seleccionado(global_names_reactivos.get_name_file_db())
        #if global_names_reactivos.get_proceso_leer_dataset():
        data = DatasetHandler.leer_dataset(global_session.get_id_user(), global_session.get_id_proyecto(), global_session.get_name_proyecto(),  global_session_V2.get_dataSet_seleccionado())
        global_session.set_data_set_reactivo(data)

 
    @output
    @render.ui
    def remove_dataset():
        list.set(get_records(table='name_files',
            columns=['id_files', 'nombre_archivo', 'fecha_de_carga'],
            join_clause='INNER JOIN version ON name_files.version_id = version.version_id',
            where_clause='version.project_id = ?',
            where_params=(global_session.get_id_proyecto(),)))
        #name.set(global_names_reactivos.get_name_file_db())
        return button_remove(list.get(), global_session.get_id_dataSet(), "id_files", name)
        
    
    @reactive.Effect
    def boton_para_eliminar_name_data_set():
        eliminar_version_id = f"eliminar_version_{global_session.get_id_dataSet()}_{name}"

        @reactive.Effect
        @reactive.event(input[eliminar_version_id])
        def eliminar_version_id():
            base_datos = 'Modeling_App.db'
            tabla = 'name_files'
            columna_objetivo = 'nombre_archivo'
            columna_filtro = 'id_files'
            nombre_version = obtener_valor_por_id(base_datos, tabla, columna_objetivo, columna_filtro, global_session.get_id_dataSet())
            #nombre_version = obtener_valor_por_id(global_session.get_id_dataSet())
            create_modal_v2(f"Seguro que quieres eliminar el Dataset {nombre_version}?", "Confirmar", "Cancelar", "confirmar_id_borrar_dataset", "cancelar_id_dataSet")
    
    
    @reactive.Effect
    @reactive.event(input["cancelar_id_dataSet"])
    def remove_modal_Dataset():
        ui.modal_remove()   
     
     
    @reactive.Effect
    @reactive.event(input.confirmar_id_borrar_dataset)
    def remove_versiones_de_parametros():
        print("estoy?")
        eliminar_version("name_files", "id_files", global_session.get_id_dataSet())
        columnas = ['id_files', 'nombre_archivo']
        tabla = "name_files"
        lista_de_versiones_new = obtener_versiones_por_proyecto(columnas,tabla)

        list.set(lista_de_versiones_new)
        ui.update_select(
            "files_select",
            choices={str(vers['id_files']): vers['nombre_archivo']
                     for vers in lista_de_versiones_new}
        )
        ui.modal_remove()
            
            
    def create_modal():
        return ui.modal(
            ui.tags.div(
                ui.row(
                    ui.column(
                        12,  # La columna ocupa toda la fila para que el contenido esté alineado correctamente
                        ui.tags.div(
                            ui.input_dark_mode(mode="light", class_="dark-mode-toggle"),
                            style="display: flex; justify-content: flex-start;"  # Alinea el contenido a la izquierda
                        )
                    ),
                    ui.column(
                        12,
                        ui.input_select(
                            "number_choice",
                            "Selecciona un número de columnas de dataset",
                            choices=[str(i) for i in range(5, 26)],
                            width="100%"
                        )
                    )
                )
            ),
            title="Configuración",
            easy_close=True,
            size='l',
            footer=ui.input_action_button("close_modal", "Cerrar")
        )


        
    @reactive.Effect
    @reactive.event(input["configuracion"])
    def modal():
        modal = create_modal()
        ui.modal_show(modal)
        
    
    @reactive.effect
    def capturar_num_seleccionador_dataSet():
        valor_Defult = "5"
        select_number_data_set = input.number_choice()
        global_estados.set_numero_dataset(select_number_data_set)
        
        
    @reactive.Effect
    @reactive.event(input["close_modal"])
    def cerrar_modal_config():
      return ui.modal_remove()