import os
from shiny import App, ui, reactive
import os
import jwt


def errores(mensaje):
    if mensaje.get():
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje.get(), style="font-style: italic;"),
            duration=None,
            close_button=True
            # type='message',
        )


def cambiarAstring(nombre_input):
    # Verificar si el input es un tuple
    input = ', '.join(map(str, nombre_input))
    print( input ,"estoy en la funcion")
    return input



def trans_nulos_adic(input_name):
    # Recorre cada valor de input_name, conviértelo a string y agrega " = 0"
    input_values = ', '.join(f"{str(value)} = 0" for value in input_name)
    print(input_values)
    return input_values

def validar_proyecto(nombre_proyecto):
    if not nombre_proyecto:  # Esto verifica si está vacío o None
        return False
    # Aquí puedes agregar más lógica de validación si es necesario
    return True  # 


def mostrar_error(mensaje_error):
    if mensaje_error:
        ui.notification_show(
            ui.p("Error:", style="color: red;"),
            action=ui.p(mensaje_error, style="font-style: italic;"),
            duration=7,
            close_button=True
        )
        
        
        
def extract_user_id(token):
    try:
        # Decodificar el token (esto no verifica la firma, solo decodifica el contenido)
        decoded_token = jwt.decode(token, options={"verify_signature": False}, algorithms=["HS256"])
        # El user_id normalmente está en el campo 'sub' del JWT
        return decoded_token.get("sub")  # Extraer el 'sub' claim (user_id)
    except jwt.DecodeError as e:
        print(f"Error al decodificar el token JWT: {e}")
        return None

# Crear carpetas por ID de usuario
def crear_carpetas_por_id_user(user_id):
    user_id_cleaned = user_id.replace('|', '_')
    base_folder_path = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    
    entrada_folder = os.path.join(base_folder_path, f"datos_entrada_{user_id_cleaned}")
    salida_folder = os.path.join(base_folder_path, f"datos_salida_{user_id_cleaned}")
    
    if not os.path.exists(entrada_folder):
        os.makedirs(entrada_folder)
        print(f"Carpeta creada {entrada_folder}")
    
    if not os.path.exists(salida_folder):
        os.makedirs(salida_folder)
        print(f"Carpeta creada {salida_folder}")
    
    return user_id_cleaned


def get_user_directory(user_id):
    base_directory = r'/mnt/c/Users/fvillanueva/Desktop/SmartModel_new_version/new_version_new/Automat'
    user_directory = os.path.join(base_directory, f'datos_entrada_{user_id}')
    return user_directory

def acomodar_mail(mail):
    email = mail
    nick = email.split('@')[0]  # Obtiene la parte antes del '@'
    print(nick)
    return nick

 # Nueva función para obtener el user_id de Auth0 usando el correo del usuario
    def obtener_user_id(access_token, email):

        conn = http.client.HTTPSConnection("dev-qpjdn3ayg3o85irl.us.auth0.com")
        
        # Prepara los headers con el token de autorización
        headers = {
            'Authorization': f"Bearer {access_token}"
        }
        
        
        # Codifica la dirección de correo electrónico
        encoded_email = urllib.parse.quote(email)
        print(email)
        print(f"Using access token: {access_token}")
        # Realiza la solicitud GET al endpoint
        conn.request("GET", f"/api/v2/users-by-email?email={encoded_email}", headers=headers)
        
        
        # Obtiene la respuesta
        res = conn.getresponse()
        print(res)
        data = res.read()
        print(data)

        # Decodifica la respuesta
        response_data = json.loads(data.decode("utf-8"))
        print(response_data)
    