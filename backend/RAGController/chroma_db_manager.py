# IMPORTACIÓN DE MÓDULOS
import os
from langchain_chroma import Chroma
from langchain.chains import ConversationalRetrievalChain
from RAGController.embeddings_model import EmbeddingsModel


class ChromaDBManager(EmbeddingsModel):

    def __init__(self, db_name="db", db_dir=r".\knowledge-base"):
        super().__init__()
        self.__db_name = db_name    # Nombre de la base de datos
        self.__db_dir = db_dir  # Ubicación de la base de datos
        # Se asegura la existencia de la carpeta que contiene a la bd
        os.makedirs(self.__db_dir, exist_ok=True)
        # Se obtiene la ruta a la base de datos
        self.__db_path = os.path.join(self.__db_dir, self.__db_name)
        # Se inicializa la conexión a la base de datos
        self.__db = Chroma(persist_directory=self.__db_path, embedding_function=self._embeddings)
        self.__collections = self.load_categories()  # Lista con el nombre de las colecciones disponibles.

    def create_collection(self, file_content: bytes, file_extension: str, category):
        try:
            # Si el nombre de la colección ya existe
            if category in self.__collections:
                return False, f"El nombre del entrenamiento {category} ya está registrado."

            # Se procesa el documento.
            text = self.process_document(file_content, file_extension)
            print(text)
            if not text:    # Si no se obtuvo el texto del documento.
                return False, f"No se logró procesar el documento proporcionado."

            # Se obtienen pedazos del texto procesado con los metadatos asignados.
            documents = self.create_embedding(text=text, category=category)

            if not documents:   # Si no se obtuvieron los pedazos con metadatos.
                return False, f"No se lograron asignar los datos al entrenamiento correspondiente."

            # Se agrega el texto dividido como incrustaciones a la base de datos.
            self.__db.add_documents(documents)
            # Se agrega el nombre a las colecciones existentes.
            self.__collections.append(category)

            return True, f"Se ha creado el entrenamiento {category}."

        except Exception as error:
            print(f">>> Error al crear una colección: {error}.")
            return False, "Ocurrió un error inesperado al crear el entrenamiento."

    def delete_collection(self, category):
        try:
            if not category in self.__collections:  # Si la colección no existe.
                return False, f"El entrenamiento no está registrado."

            # Se eliminan los documentos con los metadatos correspondientes.
            self.__db.delete(where={"category": category})
            # Se elimina el nombre del colección de la lista de colecciones.
            self.__collections.remove(category)

            return True, f"Se eliminó el entrenamiento {category}."

        except Exception as error:
            print(f"Error al eliminar la colección: {error}.")
            return False, f"Ocurrió un error inesperado al borrar el entrenamiento."

    def update_collection(self, file_content: bytes, file_extension: str, category):
        try:
            if not category in self.__collections:  # Si la colección no existe.
                return False, f"El entrenamiento no está registrado."

            # Se procesa el documento.
            text = self.process_document(file_content, file_extension)

            if not text:  # Si no se obtuvo el texto del documento.
                return False, f"No se logró procesar el documento proporcionado."

            # Se obtienen pedazos del texto procesado con los metadatos asignados.
            documents = self.create_embedding(text=text, category=category)

            if not documents:  # Si no se obtuvieron los pedazos con metadatos.
                return False, f"No se lograron asignar los datos al entrenamiento correspondiente."

            # Se agrega el texto dividido como incrustaciones a la base de datos.
            self.__db.add_documents(documents)

            return True, f"Se ha actualizado el entrenamiento {category}."

        except Exception as error:
            print(f"Error al actualizar la colección: {error}.")
            return False, f"Ocurrió un error inesperado al actualizar el entrenamiento."

    def load_categories(self):
        try:
            # Se obtienen todos los documentos de la base de datos.
            all_docs = self.__db.get(include=['metadatas'])

            categories = set()

            # Se filtran los resultados con base a sus metadatos.
            for metadata in all_docs['metadatas']:
                if metadata and "category" in metadata:
                    categories.add(metadata["category"])

            return list(categories)

        except Exception as error:
            print(f"Error al obtener los entrenamientos: {error}.")
            return []

    def db_query(self, query, category, k):
        try:
            if not category in self.__collections:  # Si el entrenamiento no existe
                return False, f"El entrenamiento {category} no está registrado."

            # Se obtiene el resultado de la consulta a la base de datos.
            results = self.__db.similarity_search(query, k=k, filter={"category": category})

            if not results: # Si no se encontraron coincidencias.
                return False, "No se encontraron resultados para la consulta en la base de datos."

            return True, [res.page_content for res in results]

        except Exception as error:
            print(f">>> Error al consultar la base de datos: {error}.")
            return False, "Ocurrió un error inesperado al consultar la base de datos."

    def get_collections(self):
        """
        Método encargado de retornar la lista de colecciones disponibles en la base de datos.
        """
        return self.__collections
