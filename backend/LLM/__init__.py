from dotenv import load_dotenv
import os

load_dotenv()

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL")  # Modelo para generar embeddings
OLLAMAMODELS= os.getenv("OLLAMAMODELS")