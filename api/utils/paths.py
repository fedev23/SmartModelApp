def build_base_directory(user_id, id_proyecto, nombre_proyecto):
    return f"/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat/datos_salida_{user_id}/proyecto_{id_proyecto}_{nombre_proyecto}"

def build_insample_folder(base_directory, id_version, nombre_version, id_version_insample, nombre_version_insample):
    return f"{base_directory}/version_{id_version}_{nombre_version}/version_parametros_{id_version_insample}_{nombre_version_insample}"


