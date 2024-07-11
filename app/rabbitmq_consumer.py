import os 
import json
import pika
import asyncio
from app.crud.sesnsordata import get_sensor_data_by_product_code_current, get_sensor_data_by_product_code, getall, getallhystory
from app.socket_manager import sio
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import SensorData
from app.services.data_processing import DataProcessingService
from app.services.statics import DataStatictsService
from app.services.probability import DataProbability
import time
RABBITMQ_URL = os.getenv("RABBITMQ_URL")
RABBITMQ_QUEUE = os.getenv("RABBITMQ_QUEUE")
RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

async def async_callback(session, data):
    try:
        results = []
        result2 = []
       
        if data["anomalie"] is True:
            await sio.emit("anomalies",json.dumps({"message":"anomalia detectada en el panel solar con el el sensor de "+str(data["nameSensor"]),"nameSensor":data["nameSensor"],"codeOfProduct":data["codeOfProduct"],"sensorData":data}),room=data["codeOfProduct"])
        if data["sensorId"] == 1:
            results = get_sensor_data_by_product_code(session, data["codeOfProduct"], 1)
            serialized_results = [result.serialize() for result in results]
            
            frequencies, values = DataProcessingService.process_sensor_data(serialized_results)
            histogram_json = json.dumps({"success": True,
                                         "message": "Data found", "label": values, "data": frequencies, "nameSensor": "sensor de temperatura Digital Ds18b20"})
            await sio.emit("histogram", histogram_json, room=data["codeOfProduct"])
        elif data["sensorId"] == 4 or data["sensorId"] == 2:
            results = get_sensor_data_by_product_code(session, data["codeOfProduct"], 4)
            result2 = get_sensor_data_by_product_code(session, data["codeOfProduct"], 2)
            serialized_resultsone = [result.serialize() for result in results]
            serialized_resultstwo = [result.serialize() for result in result2]
            scatter_data = DataProcessingService.process_sensor_data_probabilistic(serialized_resultsone, serialized_resultstwo)
            scatter_json = json.dumps({"success": True,
                                       "message": "Data found", "data": scatter_data, "x": "modulo de sesnor de corriente Acs712", "y": "modulo de sensor de luz fotoresistencia ldr"})
            await sio.emit("scatter-plot", scatter_json, room=data["codeOfProduct"])
        else:
            # results = getall(session)
            # serialized_results = [result.serialize() for result in results]
            # line_chart_data = DataProcessingService.linechart(serialized_results)
            # line_chart_json = json.dumps({"success": True,
            #                               "message": "Data found", "data": line_chart_data})
            # await sio.emit("line-chart", line_chart_json, room=data["codeOfProduct"])
            results = getallhystory(session)
            serialized_results = [result.serialize() for result in results]
            boxplot = DataProcessingService.boxplot(serialized_results)
            boxplot_json = json.dumps({"success": True,
                                       "message": "Data found", "data": boxplot})
            staticts=DataStatictsService.meditions(serialized_results)
            staticts_json = json.dumps({
                "success": True,
                "message": "Data found",
                "data": staticts
            })
            probabilitysensor=get_sensor_data_by_product_code(session, data["codeOfProduct"], 3)
            probabilitysensor = [result.serialize() for result in probabilitysensor]
            threshold = 100
            results = DataProbability.calculate_sensor_probability(probabilitysensor, threshold)
            resultjson = json.dumps({
                "success": True,
                "message": "Data found",
                "data": results
            })
            await sio.emit("probabilitysensor", resultjson, room=data["codeOfProduct"])
            await sio.emit("meditions", staticts_json, room=data["codeOfProduct"])

            await sio.emit("boxplot", boxplot_json, room=data["codeOfProduct"])
    except Exception as e:
        print(f"Error in async_callback: {e}")

def start_rabbit_consumer():
    credentials = pika.PlainCredentials(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_URL,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300
    )

    while True:
        try:
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)

            def callback(ch, method, properties, body):
                data = json.loads(body)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                session = SessionLocal()
                loop.run_until_complete(async_callback(session, data))
                loop.close()

            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)
            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()
        except (pika.exceptions.AMQPConnectionError, pika.exceptions.ConnectionClosedByBroker):
            print("Connection closed, retrying in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}, retrying in 5 seconds...")
            time.sleep(5)
