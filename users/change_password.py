# users/change_password.py

import bcrypt
from getpass import getpass
from users.user_manager import load_users, save_users
from users.session_manager import get_current_user, get_current_role
from core.logger import logger

def change_password():
    users = load_users()
    current_user = get_current_user()
    current_role = get_current_role()

    print("🔐 Cambiar contraseña")
    target_user = input("Usuario al que deseas cambiar la contraseña: ") if current_role == "admin" else current_user

    if target_user not in users:
        print("❌ El usuario no existe.")
        return

    if current_role != "admin" or target_user == current_user:
        old_password = getpass("Contraseña actual: ")
        if not bcrypt.checkpw(old_password.encode(), users[target_user]["password"].encode()):
            print("❌ Contraseña actual incorrecta.")
            return

    new_password = getpass("Nueva contraseña: ")
    confirm = getpass("Confirma la nueva contraseña: ")

    if new_password != confirm:
        print("❌ Las contraseñas no coinciden.")
        return

    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    users[target_user]["password"] = hashed

    # No guardar la contraseña en texto plano en ningún caso, para mayor seguridad
    if "password_plana" in users[target_user]:
        users[target_user].pop("password_plana")

    save_users(users)

    logger.info(f"Contraseña cambiada para '{target_user}' por '{current_user}'.")
    print("✅ Contraseña actualizada exitosamente.")
