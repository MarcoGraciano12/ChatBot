from dotenv import load_dotenv
import os

load_dotenv()


# Definir la ruta correcta dentro de backend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtiene la carpeta actual (RAG/)
DB_DIR = os.path.join(BASE_DIR, "..", "GFDB")  # Subimos un nivel y buscamos GFDB

DB_DIR = os.path.abspath(DB_DIR)  # Convertimos a ruta absoluta

print(f">>> Buscando base de datos en: {DB_DIR}")

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", None)  # Modelo para generar embeddings
DATABASE = "../knowledge-base"