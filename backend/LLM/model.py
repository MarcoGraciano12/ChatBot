import ollama
from RAG.manager import RAGDataHandler
from LLM import OLLAMAMODELS

class OllamaModelSingleton:
    _instance = None  # Aquí se guarda la instancia única del modelo

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Solo se crea la instancia del modelo la primera vez que se llama
            cls._instance = super(OllamaModelSingleton, cls).__new__(cls, *args, **kwargs)
            cls._instance.model = ollama  # Inicializas el modelo aquí (cargado solo una vez)
        return cls._instance


class OllamaChatManager:

    def __init__(self):
        self.manager = RAGDataHandler()
        self.model_instance = OllamaModelSingleton()
        self.ollama_models = OLLAMAMODELS.split(',')
        self.model_selected = None


    def load_model_chat(self, index: int):
        try:
            self.model_selected = self.ollama_models[index]
        except Exception as e:
            print(e)

    def query_model(self, query: str):
        contexto = """
        Eres un asistente virutal que trabaja para Grupo Fórmula, una empresa mexicana. Las personas acuden a ti para
        realizarte preguntas, responde de manera amable a las personas.
        """
        try:
            response = self.model_instance.model.chat(model=self.model_selected,
                                                 messages=[
                                                     {'role': 'system', 'content': f'{contexto}'},
                                                     {'role': 'user', 'content': query},
                                                 ],
                                                 stream=True)

            # for chunk in response:
            #     print(chunk['message']['content'], end='', flush=True)
            for chunk in response:
                yield chunk['message']['content']
        except Exception as e:
            print(e)

def seleccionar_modelo():
    while True:
        print("Modelos Disponibles:\n")
        for index, model in enumerate(chat_manager.ollama_models):
            print(f"{index}) {model}")
        try:
            model_option = int(input("Selecciona un modelo de los disponibles:\t"))

            if model_option < len(chat_manager.ollama_models):
                return model_option

            print("Opción inválida, verifica los módelos disponibles en el ménú.")
        except Exception as e:
            print(f"La opción ingresa no se encuentra en el formato solicitado: {e}")



if __name__ == "__main__":
    chat_manager = OllamaChatManager()
    model_option = seleccionar_modelo()
    chat_manager.load_model_chat(model_option)
    while True:
        try:
            user_query = input("\nTú:\t")

            if user_query.lower() == "salir":
                break

            if user_query.lower() == "cambiar modelo":
                model_option = seleccionar_modelo()
                chat_manager.load_model_chat(model_option)
                continue  # Evita que se envíe "cambiar modelo" al chat

            print(f"🤖 {chat_manager.ollama_models[model_option]}")
            chat_manager.query_model(user_query)
        except Exception as e:
            print(e)






