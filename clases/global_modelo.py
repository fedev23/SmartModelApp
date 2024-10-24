from clases.class_modelo import ModeloProceso

# Crea la instancia global de ModeloProceso
global_desarollo = ModeloProceso(
    nombre="desarollo",
    directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
    name_file = "", 
    mensaje_id = "mensaje_desarrollo",
    script_name="",
    script_path=""
)


modelo_of_sample = ModeloProceso(
        nombre="of_sample",
        name_file = "", 
        mensaje_id= "mensaje_of_sample",
        directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
        script_name="Levantar_Contenedor.sh",
        script_path="./Validar_Nueva.sh datos_entrada datos_salida"
    )



modelo_produccion = ModeloProceso(
        nombre="produccion",
        name_file = "",
        mensaje_id= "mensaje_produccion", 
        directorio=r"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat",
        script_name="Levantar_Contenedor.sh",
        script_path="./Scoring.sh datos_entrada datos_salida"
    )


