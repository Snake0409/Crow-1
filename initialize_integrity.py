import os
from core.integrity import initialize_integrity

FILES_TO_CHECK = [
    os.path.join(os.path.dirname(__file__), "main.py"),
    os.path.join(os.path.dirname(__file__), "core", "integrity.py"),
    # Añade aquí otros archivos críticos que quieras proteger
]

if __name__ == "__main__":
    initialize_integrity(FILES_TO_CHECK)
    print("✔️ Integridad inicializada y hashes guardados.")
