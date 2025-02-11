
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
    print(f"\n🔍 Ejecutando `manejo_de_ultimo_seleccionado` para {input_select_name}")
    print(f"📌 input_select_value: {input_select_value}")

    if is_initializing():
        print(f"⚡ Inicialización detectada para {input_select_name}")
        is_initializing.set(False)  # Marcar como inicializado

        # Obtener el último ID almacenado
        ultimo_id = ultimo_id_func()
        print(f"📌 Último ID almacenado obtenido: {ultimo_id}")

        if ultimo_id:
            print(f"✅ Último ID existente: {ultimo_id}, actualizando global...")
            global_set_func(ultimo_id)

            # Obtener el último valor almacenado en la DB
            ultimo_select = obtener_ultimo_func(db_table, db_column_name)
            print(f"📌 Último valor obtenido desde la BD: {ultimo_select}")

            # Obtener opciones disponibles y mapear clave
            opciones = obtener_opciones_func()
            print(f"📌 Opciones obtenidas: {opciones}")

            key_match = mapear_clave_func(ultimo_select, opciones)
            print(f"🔎 Clave mapeada en opciones: {key_match}")

            # Actualizar selector en la UI
            selected_value = key_match if key_match else next(iter(ultimo_select), "")
            print(f"📌 Valor seleccionado para la UI: {selected_value}")

            ui_update_func(input_select_name, choices=opciones, selected=selected_value)
        
        else:
            print(f"⚠️ No hay último ID, usando input_select_value: {input_select_value}")
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)

        return

    # Lógica para cambios explícitos en el selector
    print(f"📌 Revisando cambios explícitos en selector...")
    ultimo_id = ultimo_id_func()
    print(f"📌 Último ID después de la inicialización: {ultimo_id}")

    if ultimo_id:
        if ultimo_id != input_select_value:
            print(f"⚡ Cambio detectado: {ultimo_id} -> {input_select_value}")
            global_set_func(input_select_value)
            actualizar_ultimo_func(db_table, db_column_id, input_select_value)
        else:
            print(f"✅ No hay cambios en el selector, mantiene: {ultimo_id}")
    else:
        print(f"⚠️ No hay último ID, actualizando con input_select_value: {input_select_value}")
        global_set_func(input_select_value)
        actualizar_ultimo_func(db_table, db_column_id, input_select_value)
