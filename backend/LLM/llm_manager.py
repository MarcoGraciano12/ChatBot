import ollama
from RAG.manager import RAGDataHandler
from LLM import OLLAMAMODELS


class OllamaSingleton:
    """Patrón Singleton para mantener la instancia de Ollama y reducir tiempos de carga."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(OllamaSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = ollama  # Mantener la instancia única de Ollama
        return cls._instance


class ModelManager:
    """Gestiona la carga y selección de modelos."""

    def __init__(self):
        self.available_models = [model.strip() for model in OLLAMAMODELS.split(',')]
        self.selected_model = self.available_models[0]  # Modelo por defecto
        self.ollama_instance = OllamaSingleton()

    def load_model(self, index: int):
        """Selecciona un modelo de la lista."""
        if 0 <= index < len(self.available_models):
            self.selected_model = self.available_models[index]
            print(f"✅ Modelo cambiado a: {self.selected_model}")
        else:
            print("❌ Error: Índice de modelo fuera de rango.")


class ChatSession:
    """Maneja la interacción con el modelo seleccionado."""

    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.ollama_instance = OllamaSingleton()
        self.rag_handler = RAGDataHandler()  # Si se requiere para procesamiento adicional

    def query_model(self, query: str, rag=1, level=1):
        """Envía la consulta al modelo y devuelve el stream de respuesta."""
        if not query.strip():
            print("⚠️ No puedes enviar un mensaje vacío.")
            return

        response_level = ["debes responder de la forma más breve posible, mientras menos palabras mejor.",
                          "debes responder de forma directa y no tan extenso.",
                          "debes de proporcionar una respuesta expandida y sin inventar nada."]

        db_consult = "\n".join(self.rag_handler.query_db(query,rag))

        contexto = ("Eres un asistente virutal de Grupo Fórmula. El usuario te hará una pregunta y deberás"
                    " responder con base al contexto y nada más. El contexto que necesitas para responder la pregunta es"
                    f": {db_consult}. Recuerda: {response_level[level]}")
        try:
            response = self.ollama_instance.client.chat(
                model=self.model_manager.selected_model,
                messages=[
                    {'role': 'system', 'content': contexto},
                    {'role': 'user', 'content': query},
                ],
                stream=True
            )
            for chunk in response:
                yield chunk['message']['content']
        except Exception as e:
            print(f"❌ Error al consultar el modelo: {e}")


if __name__ == "__main__":
    manager = ModelManager()
    chat = ChatSession(manager)

    while True:
        user_input = input("\nTú: ").strip()

        if user_input.lower() == "cambiar modelo":
            print("\n📌 Modelos disponibles:")
            for index, item in enumerate(manager.available_models):
                print(f"{index}) {item}")

            try:
                model_index = int(input("Selecciona un modelo: ").strip())
                manager.load_model(model_index)
            except ValueError:
                print("❌ Error: Ingresa un número válido.")

        elif user_input.lower() == "salir":
            print("👋 Saliendo del chat...")
            break

        elif user_input:
            print(f"\n🤖 {manager.selected_model}: ", end='', flush=True)
            for text in chat.query_model(user_input):
                print(text, end='', flush=True)
            print()  # Salto de línea después de la respuesta
