# IMPORTACIÓN DE MÓDULOS
import fitz  # PyMuPDF para PDF
import docx
import io
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.chains import ConversationalRetrievalChain


class EmbeddingsModel:

    def __init__(self, model_name="sentence-transformers/multi-qa-MiniLM-L6-cos-v1", chunk_size=256, chunk_overlap=51):
        self.__embeddings_model_name = model_name
        # Se define el modelo de incrustaciones que se estará utilizando
        self._embeddings = HuggingFaceEmbeddings(model_name=self.__embeddings_model_name)
        # Se establece la cantidad de información que contendrá cada vector
        self._text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    @staticmethod
    def extract_pdf_text(file_content: bytes):
        """
        Extrae texto de un archivo PDF usando PyMuPDF.

        :return: Texto extraído del archivo PDF.
        """
        text_buffer = io.StringIO()
        with fitz.open(stream=file_content, filetype="pdf") as doc:
            for page in doc:
                text_buffer.write(page.get_text())
        return text_buffer.getvalue()

    @staticmethod
    def extract_txt_text(file_content: bytes):
        """
        Extrae texto de un archivo TXT.

        :return: Texto extraído del archivo TXT.
        """
        return file_content.decode("utf-8", errors="ignore")

    @staticmethod
    def extract_docx_text(file_content: bytes):
        """
        Extrae texto de un archivo DOCX.

        :return: Texto extraído del archivo DOCX.
        """
        file_stream = io.BytesIO(file_content)
        doc = docx.Document(file_stream)
        return "\n".join(para.text for para in doc.paragraphs if para.text.strip())

    def process_document(self, file_content: bytes, file_extension: str):
        """
        Determina el tipo de archivo y llama al método adecuado para extraer el texto.

        :return: Texto extraído del archivo.
        :raises ValueError: Si el formato del archivo no es compatible.
        """
        try:
            if file_extension == 'pdf':
                return self.extract_pdf_text(file_content)
            elif file_extension == 'txt':
                return self.extract_txt_text(file_content)
            elif file_extension == 'docx':
                return self.extract_docx_text(file_content)
            else:
                print(f">>> Formato no soportado.")
                return None

        except Exception as e:
            print(f">>> Error al procesar el documento: {e}.")
            return None

    def create_embedding(self, text, category):
        try:
            text_chunks = self._text_splitter.split_text(text)
            documents = [Document(page_content=chunk, metadata={"category": category}) for chunk in text_chunks]
            return documents
        except Exception as e:
            print(f">>> Error al crear las incrustaciones: {e}.")
            return None
