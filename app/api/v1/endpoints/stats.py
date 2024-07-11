# app/api/v1/endpoints/stats.py

from fastapi import APIRouter, Request
import pandas as pd
import json
from app.services.data_processing import DataProcessingService
from fastapi.responses import JSONResponse

import matplotlib.pyplot as plt
router = APIRouter()

@router.post("/histogram")
async def calculate_stats(request: Request):
  try:
    data = await request.json()
    sensor_values = data.get("sensor_values", [])
    # Procesar los datos del sensor en pandas

    # Create an array of values for plotting
    frequencies, values = DataProcessingService.process_sensor_data(sensor_values)
    # Convert histogram data to JSON format
    histogram_json = json.dumps({"label": values, "data": frequencies})

    return histogram_json
  except Exception as e:
    return JSONResponse(status_code=500, content={"message": str(e)})


@router.post("/scatter-plot")
async def scatter_plot(request: Request):
  try:
    data = await request.json()
    sensor_data1 = data.get("sensor_data1", [])
    sensor_data2 = data.get("sensor_data2", [])
    # Process sensor data in pandas
    scatter_data = DataProcessingService.process_sensor_data_probabilistic(sensor_data1, sensor_data2)
    # Convert scatter data to JSON format
    scatter_json = json.dumps({"data": scatter_data, "x": sensor_data1[0]["nameSensor"], "y": sensor_data2[0]["nameSensor"]})

    return scatter_json
  except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/line-chart")
async def line_chart(request: Request):
  try:
    data = await request.json()
    sensor_data = data.get("sensor_data", [])
    # Process sensor data in pandas
    line_chart_data = DataProcessingService.linechart(sensor_data)
    # Convert line chart data to JSON format
    line_chart_json = json.dumps(line_chart_data)

    return line_chart_json
  except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})

@router.post("/frecuencytable")
async def frecuencymethod(request: Request):
  try:
    data = await request.json()
    sensor_data = data.get("sensor_data", [])
    table_frequency=DataProcessingService.frequency_table(sensor_data)
    table_frequency_json = json.dumps(table_frequency)
    return table_frequency_json
  except Exception as e:
            return JSONResponse(status_code=500, content={"message": str(e)})
@router.post("/boxplot")
async def boxplotmethod(request: Request):
  try:
    data = await request.json()
    sensor_data = data.get("sensor_data", [])
    boxplot=DataProcessingService.boxplot(sensor_data)
    boxplot_json = json.dumps(boxplot)
  
    return boxplot_json
  except Exception as e:
                return JSONResponse(status_code=500, content={"message": str(e)})






