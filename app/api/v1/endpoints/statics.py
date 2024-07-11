from fastapi import APIRouter, Request
import pandas as pd
import json
from app.crud.sesnsordata import get_sensor_data_by_product_code_current
from app.services.statics import DataStatictsService
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi import Depends

from app.database import get_db
router = APIRouter()

@router.get("/")

async def hello():
    return {"hello": "world"}
@router.post("/meditions")
async def meditions(request: Request,db: Session = Depends(get_db)):
  try:
    data = await request.json()
    

    meditions = data.get("sensor_data", [])
    
    results = DataStatictsService.meditions(meditions)
    resultjson=json.dumps(results)
    return resultjson
  except Exception as e:
    print(e)
    return JSONResponse(status_code=500, content={"message": str(e)})

    

