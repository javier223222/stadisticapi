from fastapi import APIRouter, Request
import pandas as pd
import json
from app.services.probability import DataProbability
from fastapi.responses import JSONResponse
router=APIRouter()
@router.post("/temporalSeries")
async def temporalSeries(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.temporalSeries(datarecive)
    resultjson=json.dumps({"forecast":results})
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
  
    
    
     
@router.post("/probabilitysensor")
async def probabilitysensor(request: Request):
 try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    threshold = data.get("threshold")
    print(threshold)
    results = DataProbability.calculate_sensor_probability(datarecive, threshold)
    resultjson=json.dumps(results)
    return resultjson
 except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/predictfault")
async def predictfault(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.predict_fault(datarecive)
    resultjson=json.dumps({"predict":results})
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/detectanomalies")
async def detectanomalies(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.detect_anomalies(datarecive)
    resultjson=json.dumps({"anomalies":results})
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})  
@router.post("/prrobabilityknearest")
async def prrobabilityknearest(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    k=data.get("k",0)
    results = DataProbability.k_nearest_neighbors(datarecive,k)
    resultjson=json.dumps({"anomalies":results,"k":3,"nameSensor":datarecive[0]["nameSensor"]})
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/probabilitypca")
async def probabilitypca(request: Request):
   try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.perform_pca(datarecive)
    resultjson=json.dumps({"anomalies":results})
    return resultjson
   except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/probabilitybymontecarlo")
async def probabilitybymontecarlo(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.monecarlo(datarecive)
    resultjson=json.dumps({"Probabilidad de falla":results,
                            "nameSensor":datarecive[0]["nameSensor"],
                            "porcentaje":round(results*100,2),
                            

                            })
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/probabilitybypoisson")
async def probabilityBuPoisonMethod(request: Request):
  try:
    data = await request.json()
    datarecive = data.get("sensor_data", [])
    results = DataProbability.calculate_poisson_probability(datarecive)
    resultjson=json.dumps({"Probabilidad de falla":results,
                            "nameSensor":datarecive[0]["nameSensor"],
                            "porcentaje":round(results*100,2),
                            })
    return resultjson
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})
