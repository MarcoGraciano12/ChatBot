import os
import shutil
import time
from multiprocessing import Pool
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.schema import Document
from RAG import DB_DIR, EMBEDDINGS_MODEL, DATABASE


class RAGDataHandler:
    """
    Clase para manejar la base de datos de un sistema RAG (Retrieval-Augmented Generation).

    Esta clase permite:
    - Crear una base de datos con documentos procesados y embeddings generados.
    - Cargar la base de datos sin necesidad de recargarla en cada consulta (Singleton).
    - Actualizar y eliminar la base de datos si es necesario.
    - Realizar consultas eficientes a la base de datos utilizando búsqueda semántica.

    Implementa el patrón **Singleton**, asegurando que solo haya **una instancia** en memoria.
    """

    def __init__(self):
        """
        Inicializa el manejador con el modelo de embeddings.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)
        self.db = None  # La base de datos se cargará bajo demanda.

    _instance = None  # Variable de clase para almacenar la única instancia de la clase.

    def __new__(cls, *args, **kwargs):
        """
        Método especial que implementa el patrón Singleton.
        Si ya existe una instancia de la clase, la devuelve en lugar de crear una nueva.
        """

        if cls._instance is None:
            cls._instance = super(RAGDataHandler, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Inicializa el objeto RAGDataHandler. Se ejecuta solo una vez por Singleton.
        """
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDINGS_MODEL)

    def create_db(self):
        """
         Crea una base de datos de Chroma a partir de documentos en texto plano.

        - Si la base de datos ya existe, se elimina antes de recrearla.
        - Los documentos se procesan en paralelo para mejorar el rendimiento.
        - Se almacenan en ChromaDB con sus respectivos embeddings.

        :return: True si la base de datos se creó correctamente, False en caso de error.
        """
        if os.path.exists(DB_DIR):
            print(">>> La base de datos ya existe. Eliminando para recrearla...")
            self.delete_db()

        try:
            loader = DirectoryLoader(DATABASE, glob="**/*.txt", recursive=True)
            docs = loader.load()

            if not docs:
                raise FileNotFoundError("No se encontraron documentos en la carpeta especificada.")

            print(f"{len(docs)} documentos cargados. Procesando...")

            # Procesamiento paralelo de documentos para mejorar rendimiento.
            with Pool() as pool:
                processed_docs = pool.map(self._process_document, docs)

            # Aplanar la lista de listas en una sola lista de objetos Document.
            documents = [doc for sublist in processed_docs for doc in sublist]

            if not documents:
                raise ValueError(">>> No se generaron documentos válidos después del procesamiento.")

            print(f">>> {len(documents)} fragmentos procesados. Creando base de datos...")

            # Crear la base de datos en Chroma
            Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                persist_directory=DB_DIR)

            print(f">>> Base de datos creada exitosamente.")
            return True

        except Exception as e:
            print(f">>> Error al crear la base de datos: {e}")
            return False

    @staticmethod
    def _process_document(doc):
        """
        Divide un documento en fragmentos y crea objetos `Document` con metadatos.

        :param doc: Documento original cargado desde un archivo.
        :return: Lista de objetos `Document` con fragmentos de texto y metadatos.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=100)
        split_texts = text_splitter.split_text(doc.page_content)

        return [Document(page_content=text, metadata=doc.metadata) for text in split_texts]

    def update_db(self):
        """
        Actualiza la base de datos eliminándola y recreándola.

        :return: True si la actualización fue exitosa, False en caso de error.
        """
        print(f">>> Actualizando base de datos...")
        if self.delete_db():
            return self.create_db()
        return False

    @staticmethod
    def delete_db():
        """
         Elimina la base de datos si existe, asegurando que no haya procesos bloqueándola.

        :return: True si se eliminó correctamente, False en caso de error.
        """
        try:
            if os.path.exists(DB_DIR):
                # Asegurar que ChromaDB esté completamente cerrado antes de eliminar

                time.sleep(1)  # Pequeña pausa para liberar los archivos

                # Usar shutil.rmtree() para eliminar la carpeta completa
                shutil.rmtree(DB_DIR, ignore_errors=True)
                print(">>> Base de datos eliminada correctamente.")
                return True
            else:
                print(">>> No se encontró la base de datos para eliminar.")
                return False
        except Exception as e:
            print(f">>> Error al eliminar la base de datos: {e}")
            return False

    def load_db(self):
        """
        Carga la base de datos desde el directorio persistente.

        - Si la base de datos ya está en memoria, la reutiliza.
        - Si la base de datos no existe, devuelve un error.

        :return: Instancia de `Chroma` si se carga correctamente, False en caso de error.
        """
        if self.db is None:
            try:
                if not os.path.exists(DB_DIR):
                    raise FileNotFoundError("La base de datos no existe. Crea una antes de cargarla.")

                self.db = Chroma(persist_directory=DB_DIR, embedding_function=self.embeddings)
                print(">>> Base de datos cargada exitosamente.")

            except Exception as e:
                print(f"Error al cargar la base de datos: {e}")
                return False

        return self.db

    def query_db(self, query, k=7):
        """
        Realiza una consulta en la base de datos y devuelve los documentos más relevantes.

        :param query: Texto de la consulta.
        :param k: Número de resultados más relevantes a devolver.
        :return: Lista con el contenido de los documentos encontrados.
        """
        try:
            db = self.load_db()
            if not db:
                return []

            retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
            results = retriever.invoke(query)

            print(f">>> Consulta: '{query}' - {len(results)} resultados encontrados.")
            return [doc.page_content for doc in results]

        except Exception as e:
            print(f">>> Error en la consulta: {e}")
            return []

    def debug_db(self):
        """
        Modo interactivo de depuración de la base de datos.

        - Permite realizar consultas manuales en tiempo real.
        - Escribe "salir" para terminar la sesión.
        """
        try:

            while True:
                user = input("Tu:\t")

                if user == "salir":
                    break

                response = self.query_db(user)

                if response:
                    for text in response:
                        print(text)

        except Exception as e:
            print(f"Error en la depuración de la base de datos: {e}")


if __name__ == "__main__":
    rag = RAGDataHandler()
    rag.debug_db()