FROM python:3.10-slim

# Establece el directorio de trabajo.
WORKDIR /root/airflow

# Establece la variable de entorno AIRFLOW_HOME.
ENV AIRFLOW_HOME=/root/airflow


# Instala Apache Airflow y las librerías del lab (--no-cache-dir para que la imagen sea más liviana).
RUN pip install --no-cache-dir apache-airflow scikit-learn pandas numpy pyarrow

# Inicializa la base de datos de metadata.
RUN airflow db migrate

# Copiar la carpeta de DAGs al contenedor.
COPY ./dags $AIRFLOW_HOME/dags

# Expone el puerto 8080 para el servidor web de Airflow.
EXPOSE 8080


CMD ["airflow", "standalone"]
