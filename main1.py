# main.py

# ====== IMPORTACIONES ======

# Librerías estándar de Python
import os
import sys
import cmd
import time
import threading
import getpass
import warnings

# Ajustes iniciales
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
warnings.filterwarnings("ignore", category=UserWarning)

# Librerías externas
from dotenv import load_dotenv

# ====== IMPORTACIONES INTERNAS ======

# Comandos básicos
from commands.basic_commands import (
    COMMANDS, buscar_google, mostrar_hora, saludo, ayuda
)
from commands.file_manager import (
    listar_archivos, crear_archivo, leer_archivo, eliminar_archivo
)
from commands.system_control import (
    lock_screen, shutdown, restart, logout, suspend, hibernate,
    airplane_mode, wifi_on, wifi_off, bluetooth_on, bluetooth_off
)
from commands import (
    file_unlocker,
    network_scanner,
    brute_force
)

# Herramientas de seguridad / hacking
from tools.cracking import malware_tools
from tools.cracking.hacking.offensive import pdf_unlocker
from tools.malware_sim import keylogger

# Audio
from core.audio.coqui_tts import hablar

# Mirofono\ Transcripción
from core.microfono.whisper_tts import transcribir_audio
from core.microfono.wake_word import iniciar_wakeword

# Núcleo del sistema
from core.logger import logger
from core.logic import ejecutar_comando, procesar_entrada_natural

from core.nlp_interpreter import interpretar_entrada, agregar_nueva_frase
from core.utils import ejecutar_comando_sistema, COMANDOS_SISTEMA
from core.integrity import verify_integrity
from core.user_activity import log_user_action, get_user_actions

# Gestión de usuarios y sesiones
from users.session_manager import get_current_user, start_session
from users.user_manager import (
    verify_user, register_user, change_user_role,
    delete_user, load_users, mostrar_usuarios_contrasenas
)
from users.change_password import change_password




# ====== CONSTANTES ======

FILES_TO_CHECK = [
    os.path.join(os.path.dirname(__file__), "main.py"),
    os.path.join(os.path.dirname(__file__), "core", "integrity.py"),
    # Añade aquí otros archivos críticos
]

# ====== VARIABLES GLOBALES ======
modo_seguro = False

# ====== FUNCIONES AUXILIARES ======

def login():
    print("🔐 Iniciar sesión en Proyecto Crow")
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    success, result = verify_user(username, password)

    if not success:
        logger.warning(f"Fallo en el inicio de sesión para '{username}'.")
        print(f"❌ Error: {result}")
        return None, None

    logger.info(f"Usuario '{username}' inició sesión como {result}.")

    # Determinar rol visible y saludo
    if username.lower() == "snake":
        rol_visible = "The Crow"
        try:
            hablar(f"Bienvenido de nuevo Ez-néi-k." "Crou esta en perfecto estado." "¿cómo estás hoy?")
            
        except Exception as e:
            print(f"❌ Error en saludo: {e}")
    else:
        rol_visible = result
        try:
            hablar(f"Hola {username}, soy Proyecto Crow, creado por Snake.")
            hablar("¿En qué puedo ayudarte hoy?")
        except Exception as e:
            print(f"❌ Error en saludo: {e}")

    print(f"✅ Bienvenido, {username}. Rol: {rol_visible} 🦅\n")
    log_user_action(username, "Inició sesión")
    return username, rol_visible  # 🔹 Devuelve siempre una tupla



def create_user():
    if modo_seguro:
        print("⚠️ Modo seguro activo: No se pueden crear usuarios.")
        return
    print("\n🆕 Crear nuevo usuario")
    username = input("Nombre de usuario: ")
    password = getpass.getpass("Contraseña: ")
    role = input("Rol (user/admin): ").strip().lower()
    if role not in ["user", "admin"]:
        print("❌ Rol inválido. Usando 'user' por defecto.")
        role = "user"
    success, msg = register_user(username, password, role)
    print(msg)

def update_user_role(current_user):
    if modo_seguro:
        print("⚠️ Modo seguro activo: No se pueden cambiar roles.")
        return
    print("\n🔄 Cambiar rol de usuario")
    target_user = input("Usuario a modificar: ")
    new_role = input("Nuevo rol (user/admin): ").strip().lower()
    success, msg = change_user_role(current_user, target_user, new_role)
    print(msg)

def delete_existing_user(current_user):
    if modo_seguro:
        print("⚠️ Modo seguro activo: No se pueden eliminar usuarios.")
        return
    print("\n❌ Eliminar usuario")
    target_user = input("Usuario a eliminar: ")
    success, msg = delete_user(current_user, target_user)
    print(msg)

def mostrar_menu(user, role):
    print("\n📋 Menú principal")
    print("1. Cambiar tu contraseña")

    roles_admin = ["admin", "the crow"]
    if user == "snake" or role.lower() in roles_admin:
        print("2. Cambiar la contraseña de otro usuario")
        print("3. Crear un nuevo usuario")
        print("4. Cambiar rol de un usuario")
        print("5. Eliminar un usuario")

        # Opción extra solo para snake
        if user == "snake":
            print("6. Información sobre usuarios")

        # Opciones de Pentesting / Hacking solo para The Crow y snake
        if role.lower() == "the crow" and user == "snake":
            print("\n💻 Hacking Tools")
            print("  Ofensivos:")
            print("    - unlock pdf ruta_entrada.pdf: ruta_salida.pdf  → Eliminar DRM de PDF")
            # Aquí puedes agregar más comandos ofensivos si quieres
            print("  Defensivos:")
            print("    - [Próximamente]")

            print("\n7. Malware (Opciones avanzadas de pentesting)")

    print("\nEscribe 'ayuda' para ver comandos generales o 'salir' para salir.\n")



 # ====== MODULO MALWARE (KEYLOGGER) ======
keylogger_activo = False

def activar_keylogger():
    global keylogger_activo
    if not keylogger_activo:
        keylogger.ejecutar_en_fondo()
        keylogger_activo = True
        return "🟢 Keylogger activado."
    else:
        return "🟡 Keylogger ya estaba activo."

def desactivar_keylogger():
    global keylogger_activo
    if keylogger_activo:
        # pynput no permite detener listener fácilmente, se podría mejorar
        keylogger_activo = False
        return "🔴 Intento de desactivar keylogger (puede que no se detenga realmente)."
    else:
        return "🔴 Keylogger ya estaba desactivado."



def generar_ayuda(usuario, rol):
    ayuda = {
        "🤖 Básicos": sorted([f"- {cmd}" for cmd in COMMANDS]),
        "🔍 Búsqueda e IA": [
            "- buscar [pregunta]",
            "- crow [pregunta]"
        ],
        "🗂️ Archivos": [
            "- listar archivos [ruta_opcional]",
            "- crear archivo nombre.txt:contenido",
            "- leer archivo nombre.txt",
            "- eliminar archivo nombre.txt",
        ],
        "💻 Control del sistema": [],
        "⚙️ Administración": [],
        "💻 Hacking Ético": [],
        "🧪 Malware (The Crow)": [],  # <- NUEVA SECCIÓN
        "🚪 Otros": [
            "- salir (cerrar sesión)"
        ]
    }

    # Comandos de sistema (ordenar sin duplicados)
    frases_ya_agregadas = set()
    for frases, _ in COMANDOS_SISTEMA.items():
        for frase in frases:
            frase_simple = frase.split()[0]
            if frase_simple not in frases_ya_agregadas:
                ayuda["💻 Control del sistema"].append(f"- {frase}")
                frases_ya_agregadas.add(frase_simple)

    # Comandos administrativos
    if rol in "admin" or usuario == "snake":
        ayuda["⚙️ Administración"].extend([
            "- 1 Cambiar tu contraseña",
            "- 2 Cambiar la contraseña de otro usuario",
            "- 3 Crear un nuevo usuario",
            "- 4 Cambiar rol de un usuario",
            "- 5 Eliminar un usuario",
            "- 6 Información sobre usuarios"
        ])
    else:
        ayuda["⚙️ Administración"].append("- 1 Cambiar tu contraseña")

    # Comandos de hacking ético
    if rol in ["admin", "the crow"] or usuario == "snake":
        ayuda["💻 Hacking Ético"].extend([
            "- escanear",
            "- puertos [IP]",
            "- vuln [IP]",
            "- brute ssh [IP]",
            "- brute ftp [IP]"
        ])

    # Comandos de malware solo si es The Crow
    if usuario == "snake" and rol == "the crow":
        ayuda["🧪 Malware (The Crow)"].extend([
            "- activar keylogger",
            "- capturar pantalla",
            "- detener keylogger"
        ])

    return ayuda


# ====== FUNCIÓN PRINCIPAL ======

def main():
    global modo_seguro
    logger.info("Iniciando Proyecto Crow...")

    integrity_ok, current_hashes = verify_integrity(FILES_TO_CHECK)
    if not integrity_ok:
        modo_seguro = True
        logger.error("Integridad del código comprometida. Activando modo seguro.")
        print("⚠️ Integridad comprometida. Funciones críticas bloqueadas.")
    else:
        logger.info("Integridad del código verificada correctamente.")

    user, role = login()
    if not user:
        print("Saliendo del sistema.")
        return

    
    user = user.lower() if user else ""
    role = role.lower() if role else ""

    start_session(user, role)

    mostrar_menu(user, role)
    threading.Thread(
        target=iniciar_wakeword,
        args=(user, role),
        daemon=True
    ).start()
    ejecutar_loop_principal(user, role)


# ============================
# SECCIÓN 0: DEFINICIONES GLOBALES
# ============================

# Wake words reservadas para futura entrada por voz
WAKE_WORDS = ["crow", "cuervo"]

# Comandos fijos que siempre ejecutan algo
comandos_directos = ["1", "2", "3", "4", "5", "6", "7", "8", "ayuda", "salir"]

# Lista de comandos que Crow no debe aprender automáticamente
comandos_sin_ensenar = [
    "buscar ", "crow ", "listar archivos", "crear archivo ", "leer archivo ",
    "eliminar archivo ", "escanear", "puertos ", "vuln ", "brute ",
    "desbloquear zip ", "activar keylogger"
]

# ============================
# SECCIÓN 1: ENTRADA (TEXTO)
# ============================


def _normalizar_texto_base(texto: str) -> str:
    return " ".join(texto.lower().strip().split())


def _es_activar_modo_conversacion(texto: str) -> bool:
    t = _normalizar_texto_base(texto)
    activadores = [
        "modo conversacion",
        "crow modo conversacion",
        "crow entra en modo conversacion",
        "crow entrar en modo conversacion",
        "entra en modo conversacion",
    ]
    return t in activadores


def _es_desactivar_modo_conversacion(texto: str) -> bool:
    t = _normalizar_texto_base(texto)
    desactivadores = [
        "salir modo conversacion",
        "cerrar modo conversacion",
        "cierra modo conversacion",
        "crow cierra el modo conversacion",
        "crow cierra modo conversacion",
        "crow ya terminamos",
        "ya terminamos crow",
        "eso es todo crow",
        "crow eso es todo",
    ]
    return t in desactivadores

def ejecutar_loop_principal(user, role):
    modo_conversacion_crow = False

    while True:
        entrada_bruta = input(f"{user}@ProyectoCrow>>> ").strip()

        if not entrada_bruta:
            continue

        entrada_normalizada = _normalizar_texto_base(entrada_bruta)

        if _es_activar_modo_conversacion(entrada_normalizada):
            modo_conversacion_crow = True
            print("🟢 Modo conversación con Crow activado. Escribe tus preguntas sin 'crow'.")
            print("   Para salir: 'crow ya terminamos', 'eso es todo crow' o 'cierra modo conversacion'.")
            continue

        if modo_conversacion_crow and _es_desactivar_modo_conversacion(entrada_normalizada):
            modo_conversacion_crow = False
            print("🔴 Modo conversación con Crow desactivado.")
            continue

        # ---------------------------
        # NORMALIZACIÓN BÁSICA
        # ---------------------------
        entrada_bruta = entrada_normalizada

        if modo_conversacion_crow and entrada_bruta not in comandos_directos:
            if not entrada_bruta.startswith("crow "):
                cmd = f"crow {entrada_bruta}"
            else:
                cmd = entrada_bruta
        else:
            # ============================
            # SECCIÓN 2: INTERPRETACIÓN Y COMANDOS DIRECTOS
            # ============================

            # 1️⃣ Comandos directos
            if entrada_bruta in comandos_directos:
                cmd = entrada_bruta

            else:
                # 2️⃣ Intentar interpretar (frases aprendidas / mapeadas)
                cmd = interpretar_entrada(entrada_bruta)

                # 3️⃣ Fallback si no se pudo interpretar
                if not cmd:
                    cmd = entrada_bruta

                    # Verificamos si es un comando que NO debe enseñar
                    if not any(cmd.startswith(p) for p in comandos_sin_ensenar):
                        print("❌ No entiendo ese comando.")

                        if role.lower() in ["the crow", "admin"]:
                            confirmar = input(
                                "¿Deseas enseñarme qué comando ejecutar para esto? (s/n): "
                            ).lower()

                            if confirmar == "s":
                                nuevo_comando = input(
                                    "📝 Ingresa el comando real que debería ejecutar: "
                                ).strip().lower()

                                agregar_nueva_frase(entrada_bruta, nuevo_comando)
                                print("✅ Frase aprendida. Inténtalo de nuevo.")
                            else:
                                print("↪️ Continuando sin aprender...")

                        # Saltamos esta iteración
                        continue

        # ============================
        # SECCIÓN 3: EJECUCIÓN DE COMANDOS
        # ============================

        # DEBUG opcional
        print(f"\n🛠️ DEBUG - Comando recibido: [{cmd}]")

        # 👉 Delegamos TODA la ejecución a core/logica.py
        ejecutar_comando(cmd, user, role)






# ====== EJECUCIÓN DEL PROGRAMA ======
if __name__ == "__main__":
    main()