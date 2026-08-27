# users/session_manager.py

import json
from datetime import datetime
from users.user_manager import load_users, save_users  # Para actualizar la hora de conexión

#1 - Estado de la sesión actual
current_session = {
    "username": None,
    "role": None
}

#2 - Iniciar sesión
def start_session(username, role):
    current_session["username"] = username
    current_session["role"] = role

    # ✅ Registrar hora de conexión
    users = load_users()  # Cargar todos los usuarios
    if username in users:
        users[username]["ultima_conexion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Guardar hora actual
        save_users(users)  # Guardar cambios en el archivo
        # (Esto permite que el menú admin muestre "última conexión")

#3 - Finalizar sesión
def end_session():
    current_session["username"] = None
    current_session["role"] = None

#4 - Obtener información de la sesión
def get_current_user():
    return current_session["username"]

def get_current_role():
    return current_session["role"]
