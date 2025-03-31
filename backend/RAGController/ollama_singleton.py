# IMPORTACIÓN DE MÓDULOS
import ollama


class OllamaSingleton:
    """
    Clase encargada de facilitar la implementación del patrón de diseño Singleton.

    La finalidad de esta clase es mantener una única instancia de ollama, reduciendo
    así tiempos de respuesta y costes de memoria del sistema.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Crea una nueva instancia de la clase si no existe, de lo contrario, devuelve
        la instancia existente.
        """
        try:
            if cls._instance is None:
                cls._instance = super(OllamaSingleton, cls).__new__(cls, *args, **kwargs)
                cls._instance.client = ollama  # Mantener la instancia única de Ollama.
        except Exception as error:
            print(f">>> Error al manejar la instancia de Ollama: {error}.")
        finally:
            return cls._instance    # Se retorna la instancia de Ollama.
