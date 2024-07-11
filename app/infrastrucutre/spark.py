from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import pika
import json

def get_spark_session():
    spark = SparkSession.builder.appName("RealTimeProcessing").getOrCreate()
    return spark

def create_streaming_pipeline(spark, data):
    # sensorId,valor,nameSensor,codeOfProduct
    schema = StructType([
        StructField("createdAt", StringType(), True),
        StructField("nameSensor", StringType(), True),
        StructField("valor", FloatType(), True)

    ])

    rdd = spark.sparkContext.parallelize([json.loads(data)])
    df = spark.read.json(rdd, schema=schema)
    df.show()

    processed_df = df.groupBy("nameSensor").agg({"valor": "avg"}).withColumnRenamed("avg(valor)", "average_value")
    processed_df.show()

    # Aquí puedes continuar con el procesamiento y almacenamiento del dataframe procesado
    # processed_df.write.format("some_output_format").save("path_to_save")

def rabbitmq_listener():
    def callback(ch, method, properties, body):
        data = body.decode('utf-8')
        print(f"Received {data}")

        # Obtener una sesión de Spark
        spark = get_spark_session()
        
        # Procesar los datos recibidos
        create_streaming_pipeline(spark, data)

    # Conectar a RabbitMQ remoto con autenticación
    credentials = pika.PlainCredentials('root', 'ELTopn4590')
    parameters = pika.ConnectionParameters('52.71.63.48', 5672, '/', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Asegurarse de que la cola exista
    channel.queue_declare(queue='solary')

    # Consumir mensajes de RabbitMQ
    channel.basic_consume(queue='solary', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


