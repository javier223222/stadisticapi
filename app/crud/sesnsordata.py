from sqlalchemy.orm import Session
from app.models import SensorData
from datetime import datetime

def get_sensor_data_by_product_code_current(session: Session, product_code: str, typeSensorId: int = None):
    current_year = datetime.now().year
    sensor_data = session.query(SensorData).filter(
        SensorData.createdAt >= datetime(current_year, 1, 1),
        SensorData.createdAt <= datetime(current_year, 12, 31),
        SensorData.isDeleted == False,
        SensorData.codeOfProduct == product_code,
        
    ).all()
    return sensor_data

    
def get_sensor_data_by_product_code(session: Session, product_code: str, typeSensorId: int = None):
   
    sensor_data =  session.query(SensorData).filter(
        SensorData.isDeleted == False,
        SensorData.codeOfProduct == product_code,
        SensorData.sensorId == typeSensorId
    ).all()

    return sensor_data

def getall(session: Session):
    current_year = datetime.now().year
    sensor_data = session.query(SensorData).filter(
        SensorData.createdAt >= datetime(current_year, 1, 1),
        SensorData.createdAt <= datetime(current_year, 12, 31),
        SensorData.isDeleted == False,
        
        
    ).all()
    return sensor_data

def getallhystory(session: Session):
    sensor_data = session.query(SensorData).filter(
        SensorData.isDeleted == False,
    ).all()
    
    return sensor_data


