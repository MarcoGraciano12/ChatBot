"""
Módulo encargado de la gestión de modelos locales de Ollama para su uso dentro del sistema RAG.

Este módulo proporciona la clase `ModelManager`, que permite cargar, seleccionar y configurar modelos
de lenguaje grande (LLM) instalados localmente a través de Ollama. También gestiona parámetros relacionados
con la calidad de respuesta, la cantidad de coincidencias relevantes a recuperar (`k`) y la categoría o colección
sobre la cual se realizarán las búsquedas.
"""
from RAGController.ollama_singleton import OllamaSingleton
import json
import requests

class ModelManager:
    """
    Clase para gestionar modelos LLM locales disponibles mediante Ollama y configurar sus parámetros de uso.

    Esta clase permite:
    - Cargar la lista de modelos instalados localmente.
    - Seleccionar el modelo activo a utilizar.
    - Establecer parámetros de configuración como:
        - Nivel de precisión o profundidad en la respuesta del modelo.
        - Número de resultados relevantes (`k`) que debe recuperar el sistema RAG.
        - Categoría o colección temática para contextualizar las respuestas.
    """

    def __init__(self):

        # Variable para almacenar el modelo activo.
        self.__selected_model = None

        # Se obtiene la instancia de Ollama.
        self.ollama_instance = OllamaSingleton()

        # Se carga la lista de los modelos de Ollama disponibles.
        self.__available_models = self.load_models()['content']

        # Se establece por defecto la cantidad de coincidencias del RAG a obtener.
        self._k = 1

        # Se establece por defecto la calidad de respuesta del modelo
        self._level = 0

        # Variable para gestionar la colección sobre la cual se realizarán las búsquedas.
        self._category = None


    def load_models(self):
        """
        Método encargado de retornar la lista de modelos de Ollama que se encuentran disponibles en local.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
                - 'content' (list): Lista con los modelos de Ollama disponibles.
        """
        try:

            return {'status': True, 'message': 'Se obtuvo de manera correcta la lista de modelos.',
                    'content': [llm['model'] for llm in self.ollama_instance.client.list()['models']]}

        except Exception as error:
            return {'status': False, 'message': f'Ocurrió un error al cargar la lista de modelos: {str(error)}.',
                    'content': []}

    def get_list_models(self):
        """
        Método destinado a retornar la lista de modelos de Ollama que se encuentran en
        local
        """
        return self.__available_models

    def change_selected_model(self, index:int):
        """
        Método encargado de cambiar el modelo seleccionado para responder a las preguntas del usuario.

        Args:
            index (int): Indice que el modelo ocupa en la lista de modelos disponibles.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """
        try:
            if 0 <= index < len(self.__available_models):
                # Se asigna el nuevo modelo activo
                self.__selected_model = self.__available_models[index]
                return {'status': True, 'message': f'Se ha activado el modelo {self.__available_models[index]}.'}

            # Si no se puede cambiar el modelo
            return {'status': False,
                    'message': 'El modelo seleccionado no se encuentra dentro de la lista de modelos disponibles.'}

        except Exception as error:
            return {'status': False, 'message': f'Ocurrió´un error al intentar cambiar el modelo: {str(error)}'}

    def set_k(self, k:int):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar la
        cantidad de coincidencias del RAG.
        """
        self._k = k

    def set_level(self, level:int):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar la calidad
        de las respuestas del modelo.
        """
        self._level = level

    def set_category(self, category:str):
        """
        Método para asignar un nuevo valor a la variable encargada de gestionar
        la colección sobre la cual se realizarán las búsquedas en la base de datos.
        """
        self._category = category

    def get_selected_model(self):
        """
        Método para retornar al modelo activo.
        """
        return self.__selected_model

    def get_selected_category(self):
        """
        Método para retornar la categoría que se encuentra activa.
        """
        return self._category

    def get_k(self):
        """
        Método para retornar el número de coincidencias del RAG a obtener.
        """
        return self._k

    def get_level(self):
        """
        Método para retornar el nivel de respueta del modelo.
        """
        return self._level

    # Métodos experimentales para la gestión de modelos desde local

    def delete_model(self, llm_name: str):
        """
        Método encargado de eliminar un modelo de la lista de modelos disponibles en local.

        Args:
            llm_name (str): Nombre del modelo a eliminar.

        Returns:
            dict: Un diccionario con el estado, mensaje y resultado de la operación.
                - 'status' (bool): Estado de la operación.
                - 'message' (str): Mensaje de éxito o error.
        """

        try:
            if llm_name not in self.__available_models:
                return {'status': False, 'message': f'El modelo {llm_name} no se encuentra descargado.'}

            # Se elimina el modelo
            self.ollama_instance.client.delete(llm_name)

            # Se actualiza la lista
            self.__available_models.remove(llm_name)

            return {'status': True, 'message': f'Se eliminó de forma correcta al modelo {llm_name}.'}

        except Exception as error:
            return {'status': False,
                    'message': f'No se logró eliminar el modelo {llm_name}, se presentó el error: {str(error)}.'}


    def download_model(self, llm_name: str):
        try:
            if llm_name in self.__available_models:
                yield json.dumps({
                    'status': False,
                    'message': f'El modelo {llm_name} ya está instalado.'
                })
                return


            response = requests.post('http://localhost:11434/api/pull',
                                     json={'name': llm_name},
                                     stream=True)

            # Esto levantará una excepción si el status no es 200.
            response.raise_for_status()
            # if response.status_code != 200:
            #     yield json.dumps({'status': False, 'message': f'Error al iniciar la descarga del modelo {llm_name}'})
            #     return

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        status = data.get('status')
                        total = data.get('total', 0)
                        completed = data.get('completed', 0)
                        porcentaje = (completed / total * 100) if completed and total else None
                        yield json.dumps({
                            'status': True,
                            'message': status,
                            'progress': f'{porcentaje:.2f}%' if porcentaje else None
                        })
                        print(status, total, completed,porcentaje)
                    except json.JSONDecodeError:
                        yield json.dumps({'status': False, 'message': 'Error al procesar una línea del stream'})
                    except KeyError:
                        yield json.dumps({'status': False, 'message': 'Datos incompletos en la línea del stream'})

            # Se agrega el modelo a la lista de modelos disponibles
            self.__available_models.append(llm_name)
            yield json.dumps({'status': True, 'message': f'Modelo {llm_name} instalado correctamente.'})


        except requests.RequestException as req_error:
            yield json.dumps({'status': False, 'message': f'Error de solicitud: {str(req_error)}'})
        except json.JSONDecodeError as json_error:
            yield json.dumps({'status': False, 'message': f'Error en la respuesta JSON: {str(json_error)}'})
        except Exception as error:
            yield json.dumps({'status': False,
                              'message': f'Se presentó un error inesperado: {str(error)}'})