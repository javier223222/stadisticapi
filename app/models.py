# app/models.py

from sqlalchemy import Table, MetaData
from app.database import Base, engine
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapper
from app.database import Base, engine
metadata = MetaData()

user = Table('user', metadata, autoload_with=engine)
producto = Table('producto', metadata, autoload_with=engine)
specif_product = Table('specifproduct', metadata, autoload_with=engine)
productos_of_user = Table('productosofuser', metadata, autoload_with=engine)
role = Table('role', metadata, autoload_with=engine)
sensor = Table('sensor', metadata, autoload_with=engine)
sensor_data = Table('sensordata', metadata, autoload_with=engine)


class User(Base):
    __table__ = user

    # Define relaciones aquí si es necesario
    def serialize(self):
        return {
            'id': self.id,
            'codeOfProduct': self.codeOfProduct,
            'value': self.value,
            'timestamp': self.timestamp
        }

class Producto(Base):
    __table__ = producto

    # Define relaciones aquí si es necesario

class SpecifProduct(Base):
    __table__ = specif_product
    

    # Define relaciones aquí si es necesario

class ProductosOfUser(Base):
    __table__ = productos_of_user

    # Define relaciones aquí si es necesario

class Role(Base):
    __table__ = role

    # Define relaciones aquí si es necesario

class Sensor(Base):
    __table__ = sensor

    # Define relaciones aquí si es necesario

class SensorData(Base):
    __table__ = sensor_data
    def serialize(self):
        return {
            'id': self.id,
            'sensorId': self.sensorId,
            'isDeleted': self.isDeleted,
            "valor": float(self.valor),
            'createdAt': str(self.createdAt),
            'updatedAt': str(self.updatedAt),
            'createdBy': self.createdBy,
            'updatedBy': self.updatedBy,
            'codeOfProduct': self.codeOfProduct,
            'nameSensor': self.nameSensor

        }

    # Define relaciones aquí si es necesario