
def manejo_de_ultimo_seleccionado(
    is_initializing,
    input_select_value,
    ultimo_id_func,
    global_set_func,
    actualizar_ultimo_func,
    obtener_ultimo_func,
    obtener_opciones_func,
    mapear_clave_func,
    ui_update_func,
    input_select_name,
    db_table,
    db_column_id,
    db_column_name
):
    if is_initializing():
        print(f"Inicialización detectada para {input_select_name}")
        is_initializing.set(False)  # Marcar como inicializado

        # Configurar el selector al último valor seleccionado
        ultimo_id = ultimo_id_func()
        
        print(f"ultimo_id {ultimo_id} {input_select_name}")
        if ultimo_id:
            global_set_func(ultimo_id)
            ultimo_select = obtener_ultimo_func(db_table, db_column_name)

            # Obtener opciones y mapear clave
            opciones = obtener_opciones_func()
            key_match = mapear_clave_func(ultimo_select, opciones)

            # Actualizar el selector en la UI
            ui_update_func(
                input_select_name,
                choices=opciones,
                selected=key_match if key_match else next(iter(ultimo_select), "")
            )
        else:
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)

        return

    # Lógica para cambios explícitos en el selector
    ultimo_id = ultimo_id_func()
    if ultimo_id:
        if ultimo_id != input_select_value:
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)
    else:
        global_set_func(input_select_value)
        actualizar_ultimo_func(db_table, db_column_id, input_select_value)
