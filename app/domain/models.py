from pydantic import BaseModel

class SensorDataModel(BaseModel):
   nameSensor: str
   valor: float
   createdAt: str
   @classmethod
   def from_schema(cls, schema):
        return cls(
            nameSensor=schema.nameSensor,
            valor=schema.valor,
            createdAt=schema.createdAt
        )