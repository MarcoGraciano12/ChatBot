# Usa una imagen base de Python
FROM python:3.13

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos y los instala
COPY requirements.txt .


RUN pip install -r requirements.txt

# Copia el código de la aplicación
COPY . .

# Exponer el puerto en el que corre Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
