from shiny import ui

screen_User = ui.page_fluid(
    ui.tags.button("SmartModeling", class_="logo-button"),
    ui.output_ui("create_user_menu"),
    ui.div(
         ui.accordion(
             ui.accordion_panel(
                 "Proyectos:",
                ui.output_ui("devolver_acordeon"),
             ),
             open=False,
           
               
         ),
         
        ui.output_ui("create_sidebar"),
        #ui.h3("Tarjeta de Usuario", fillable=True)
        ui.output_ui("despligue_menu"),
    ),
     
   
)
