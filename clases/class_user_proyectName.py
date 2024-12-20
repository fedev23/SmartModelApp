from shiny import ui, reactive
from shiny.express import ui as express_ui
import re
from clases.global_session import global_session
from clases.global_name import global_name_manager
from global_names import global_name_in_Sample, global_name_desarrollo, global_name_out_of_Sample, global_name_produccion
from api.db import *
from global_names import *
from clases.reactives_name import global_names_reactivos




class User_proyect:
    def __init__(self):
        self._nombre_proyecto = reactive.Value("")
        self.click_en_continuar = reactive.Value(False)
        self.hora_new_proyect = reactive.Value()
        self.error = reactive.Value("")

    def create_modal(self):
        m = ui.modal(
            ui.row(
                ui.column(12, ui.input_text("proyecto_nombre",
                          "Seleccione un nombre de proyecto", width="100%")),
            ),
            ui.div(
                ui.div(
                    ui.input_action_button(
                        "continuar", "Continuar", class_="custom-ok-button", style="text-align: left"),
                    ui.input_action_button(
                        "cancelar", "Cancelar", class_="custom-cancel-button"),
                ),
            ),
            title="Nuevo proyecto",
            easy_close=True,
            footer=None,
            size='m',
            fade=True,
        )
        ui.modal_show(m)

    def continuar_buton(self, input):
        @reactive.Effect
        @reactive.event(input.continuar)
        def finalizar_click():
            self.click_en_continuar.set(True)
            ui.modal_remove()
            # Convertir el valor a una cadena de texto
            self.set_nombre_proyecto(input.proyecto_nombre())
            #fecha_hora_registrada = global_user_proyecto.fecha_new_proyecto()
            #self.hora_new_proyect.set(fecha_hora_registrada)
            self.click_en_continuar.set(False)

    def get_boton_continuar(self):
        return self.click_en_continuar.get()

    def get_nombre_proyecto(self):
        return self._nombre_proyecto.get()

    def set_nombre_proyecto(self, nombre_proyecto):
        self._nombre_proyecto.set(nombre_proyecto)

    def cancelar_buton(self, input):
        @reactive.effect
        @reactive.event(input.cancelar)
        def cancelar_click():
            ui.modal_remove()

    def create_value_box(self, title, value, showcase=None, title_style=None, value_style=None, box_style=None):
        title_style = title_style or "font-size: 18px; font-weight: bold;"
        value_style = value_style or "font-size: 16px;"
        box_style = box_style or "border: 2px solid #ddd; padding: 10px;"

        value_content = (
            express_ui.tags.div(value, style=value_style)
            if isinstance(value, str)
            else [express_ui.tags.div(v, style=value_style) for v in value]
        )

        return express_ui.value_box(
            showcase=showcase,
            title=express_ui.tags.div(title, style=title_style),
            value=value_content,
            style=box_style
        )

    def card_desarollo(self):
        latest_date, latest_model, latest_dataset = get_latest_execution(global_session.get_id_proyecto(), global_names_reactivos.name_desarrollo_get())
        # Verificar si hay datos para mostrar
        if not latest_dataset:
            return self.create_value_box(
                title="Desarrollo",
                value=["Aún no hay modelos generados"]
            )
        
        # Contenido a mostrar en la tarjeta
        value_content = [
            f'Datos: {latest_dataset}',
            f"Última ejecución: {latest_date}",
            #f"Modelo: {latest_model}",
        ]
        
        return self.create_value_box(
            title="Desarrollo",
            value=value_content
        )

    def card_validacion_in_sample(self):
        latest_date, latest_model, latest_dataset = get_latest_execution(global_session.get_id_proyecto(), global_names_reactivos.name_validacion_in_sample_get())
        if latest_dataset and latest_date:
            return self.create_value_box(
                title=f"{global_name_in_Sample}",
                value=[
                    f'Datos: {latest_dataset}',
                    f'Última ejecución: {latest_date}'
                ]
            )
        return self.create_value_box(
            title=f"{global_name_in_Sample}",
            value=["Aún no hay modelos generados"]
        )

    def card_out_to_sample_valid(self):
        latest_date, latest_model, latest_dataset = get_latest_execution(global_session.get_id_proyecto(), global_names_reactivos.name_validacion_of_to_sample_get())
        if latest_dataset and latest_date:
            return self.create_value_box(
                title=f"{global_name_out_of_Sample}",
                value=[
                    f'Datos: {latest_dataset}',
                    f'Última ejecución: {latest_date}'
                ]
            )
        return self.create_value_box(
            title="Out-Of-Sample",
            value=["Aún no hay modelos generados"]
        )

    def card_produccion(self):
        global_name_produccion = "produccion"
        latest_date, latest_model, latest_dataset = get_latest_execution(global_session.get_id_proyecto(), global_names_reactivos.name_produccion_get())
        if latest_dataset:
            return self.create_value_box(
                title=f"{global_name_produccion}",
                value=[
                    f'Datos: {latest_dataset}',
                    f'Última ejecución: {latest_date}'
                ]
            )
        return self.create_value_box(
            title=f"{global_name_produccion}",
            value=["Aún no hay modelos generados"]
        )
    

    def create_accordeon(self, user_id):
        projects = get_user_projects(user_id)
        if projects:
            panels = []
            for project in projects:
                sanitized_name = re.sub(r'\W|^(?=\d)', '_', project['name'])
                panels.append(
                    ui.card(
                         ui.card_header(f"Proyecto: {project['name']}, Fecha de creación: {project['created_date']}"),
                        #ui.input_action_button("eliminar_proyect", "Eliminar proyecto"),
                        self.card_desarollo(),
                        self.card_validacion_in_sample(),
                        self.card_out_to_sample_valid(),
                        self.card_produccion(),
                        ui.input_action_button(f"eliminar_proyect_{sanitized_name}", "Eliminar proyecto"),
                        id=f"card{sanitized_name}", ##TENER EN CUENTA LO DE USER ID
                        #open=False
                    )
                    
                )
               
            return ui.div(ui.card(*panels))
        else:
            return ui.div("No hay proyectos disponibles para este usuario.")
        
    
    def mostrar_nombre_proyecto_como_titulo(self, proyecto):
        if proyecto:
            return proyecto
        else:
            self.error.set("No hay proyecto asignado")
            nombre = self.error.get()
            return nombre


# Crear una instancia global de User_proyect
global_user_proyecto = User_proyect()
