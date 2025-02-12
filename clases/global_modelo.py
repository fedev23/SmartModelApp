from clases.class_modelo import ModeloProceso

# Crea la instancia global de ModeloProceso
global_desarollo = ModeloProceso(
    nombre="desarollo",
    directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
    name_file = "", 
    mensaje_id = "mensaje_desarrollo",
    script_name="",
    script_path="",
    estado= "",
    hora = "",
    porcentaje_path= "",
    script_path_tablero = ""
)

modelo_in_sample = ModeloProceso(
        nombre="in_sample",
        mensaje_id= "mensaje_id_in_sample",
        name_file = "", 
        directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
        script_name="",
        script_path="" ,
        estado= "",
        hora = "",
        porcentaje_path= "",
        script_path_tablero = ""
    )


modelo_of_sample = ModeloProceso(
        nombre="of_sample",
        name_file = "", 
        mensaje_id= "mensaje_of_sample",
        directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
        script_name="",
        script_path="",
        estado= "",
        hora = "",
        porcentaje_path= "",
        script_path_tablero = ""
        
        
    )



modelo_produccion = ModeloProceso(
        nombre="produccion",
        name_file = "",
        mensaje_id= "mensaje_produccion", 
        directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
        script_name="Levantar_Contenedor.sh",
        script_path="",
        estado= "",
        hora = "",
        porcentaje_path= "",
        script_path_tablero = ""
    )


