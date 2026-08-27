# users/user_manager.py

#1 - Importaciones necesarias
import bcrypt
import json
import os
from datetime import datetime  # <-- Import agregado para fecha y hora
from core.user_activity import get_user_actions

#2 - Ruta del archivo donde se guardan los usuarios
USER_FILE = os.path.join("data", "users.json")

#3 - Inicializa el archivo si no existe
if not os.path.exists(USER_FILE):
    with open(USER_FILE, "w") as f:
        json.dump({}, f)

#4 - Cargar usuarios
def load_users():
    with open(USER_FILE, "r") as f:
        return json.load(f)

#5 - Guardar usuarios
def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

#6 - Registrar nuevo usuario
def register_user(username, password, role="user"):
    users = load_users()

    normalized_usernames = [u.lower() for u in users.keys()]
    
    if username.lower() in normalized_usernames:
        return False, "El usuario ya existe."

    if role not in ["user", "admin"]:
        return False, "Solo roles permitidos: user, admin."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    datos_usuario = {
        "password": hashed,
        "role": role
    }

    # NO guardar contraseña en texto plano para nadie, ni Snake ni otro
    # Así mantenemos máxima seguridad y privacidad

    users[username] = datos_usuario
    save_users(users)
    return True, f"Usuario '{username}' creado con rol '{role}'."
    
#7 - Verificar usuario
def verify_user(username, password):
    users = load_users()
    if username not in users:
        return False, "Usuario no encontrado."

    stored_hash = users[username]["password"].encode()
    if bcrypt.checkpw(password.encode(), stored_hash):
        # Actualizar la última conexión cuando el login es exitoso
        users[username]["last_login"] = datetime.now().isoformat()
        save_users(users)
        return True, users[username]["role"]
    else:
        return False, "Contraseña incorrecta."

#8 - Cambiar rol
def change_user_role(requesting_user, target_user, new_role):
    users = load_users()

    if requesting_user.lower() != "snake":
        return False, "Solo Snake puede cambiar roles."

    if target_user not in users:
        return False, "El usuario objetivo no existe."

    if target_user.lower() == "snake":
        return False, "No puedes cambiar el rol de Snake."

    if new_role == "The Crow":
        return False, "Nadie más puede ser The Crow."

    users[target_user]["role"] = new_role
    save_users(users)
    return True, f"Rol de '{target_user}' cambiado a '{new_role}'."

#9 - Eliminar usuario
def delete_user(requesting_user, target_user):
    users = load_users()

    if requesting_user.lower() != "snake":
        return False, "Solo Snake puede eliminar usuarios."

    if target_user.lower() == "snake":
        return False, "No puedes eliminar a Snake."

    if target_user not in users:
        return False, "El usuario no existe."

    del users[target_user]
    save_users(users)
    return True, f"Usuario '{target_user}' eliminado correctamente."

def mostrar_usuarios_contrasenas():
    usuarios = load_users()

    print("\n🔐 Usuarios del sistema (solo para The Crow):\n")
    for usuario, datos in usuarios.items():
        print(f"- Usuario: {usuario}")
        
        # Nunca mostrar contraseña en texto plano
        print(f"  Contraseña: (Protegida)")
        
        # Última conexión
        ultima_conexion = datos.get("last_login", "(Nunca)")
        print(f"  Última conexión: {ultima_conexion}")
        
        # Últimas acciones
        acciones = get_user_actions(usuario)
        if acciones:
            print("  Últimas acciones:")
            for act in acciones:
                print(f"    - {act['timestamp']}: {act['action']}")
        else:
            print("  Sin acciones registradas.")
        
        print("-" * 40)