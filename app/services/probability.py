from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import numpy as np
from scipy.stats import norm
import pandas as pd
from prophet import Prophet
import datetime
from dotenv import load_dotenv
import os
from sklearn.decomposition import PCA
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import norm

# Cargar variables de entorno desde el archivo .env
load_dotenv()
class DataProbability:
    def temporalSeries(datarecive):
        
        data=pd.DataFrame([{
            "ds": pd.to_datetime(dp["createdAt"]).tz_localize(None),
            "y": dp["valor"]
            
        } for dp in datarecive])

        m = Prophet()
        m.fit(data)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)
        forecast['ds'] = forecast['ds'].dt.strftime('%Y-%m-%d %H:%M:%S')
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(orient='records')
        return forecast
    def calculate_sensor_probability(datareceive,threshold=None):
            # Extraer los valores de los datos recibidos
        data = [dp["valor"] for dp in datareceive]
        data = np.array(data)

    # Calcular la media y la desviación estándar de los datos
        mean = np.mean(data)
        std_dev = np.std(data)

    # Establecer umbrales si no se proporcionan
        if threshold is None:
            lower_threshold = mean - 3 * std_dev
            upper_threshold = mean + 3 * std_dev
        else:
            lower_threshold = upper_threshold = threshold
    
    # Calcular la probabilidad de estar por debajo del umbral
        prob_below_threshold = norm.cdf(threshold, mean, std_dev)

    # Calcular la probabilidad de estar fuera del rango
        prob_below_lower = norm.cdf(lower_threshold, mean, std_dev)
        prob_above_upper = 1 - norm.cdf(upper_threshold, mean, std_dev)
        prob_out_of_range = prob_below_lower + prob_above_upper
        prob_within_range = 1 - prob_out_of_range

    # Verificar si hay fallos en los datos
        is_failing = any((data < lower_threshold) | (data > upper_threshold))

    # Retornar el resultado en formato JSON
        return {
            "mean": round(mean, 3),
            "std_dev": round(std_dev, 3),
            "lower_threshold": round(lower_threshold, 3),
            "upper_threshold": round(upper_threshold, 3),
            "nameSensor": datareceive[0]["nameSensor"],
            "probability_out_of_range": round(prob_out_of_range, 3),
            "probability_within_range": round(prob_within_range, 3),
            "porcentaje_out_of_range": round(prob_out_of_range * 100, 2),
            "porcentaje_within_range": round(prob_within_range * 100, 2),
            "is_failing": is_failing,
            "probability_below_threshold": round(prob_below_threshold, 3),
            "porcentaje_below_threshold": round(prob_below_threshold * 100, 2)
             }
       
    def predict_fault(data):
        df=pd.DataFrame([{
            "ds":pd.to_datetime(dp["createdAt"]).tz_localize(None),
            "y":dp["valor"]

        } for dp in data])
        mean=df["y"].mean()
        std_dev=df["y"].std()
        def normal_probability_denity(x,mean,std):
            return 1/(std*np.sqrt(2*np.pi))*np.exp(-0.5*((x-mean)/std)**2)
        df["probability"]=df["y"].apply(lambda x: normal_probability_denity(x,mean,std_dev))
        threshold=df["probability"].quantile(0.05)
        df["anomaly"]=(df["probability"]<threshold).astype(int)
        df["ds"]=df["ds"].dt.strftime('%Y-%m-%d %H:%M:%S')
        result=df[["ds","y","anomaly"]].to_dict(orient="records")
        return result
    @staticmethod
    def detect_anomalies(data):
        df=pd.DataFrame(data)
        mean=df["valor"].mean()
        std=df["valor"].std()
        threshold=3
        
        anomaly_threshold=mean+threshold*std
        df["anomaly"]=df["valor"]>anomaly_threshold
        anomaly_values = df[df["anomaly"]]["valor"].tolist()
        
        return anomaly_values
   
    @staticmethod
    def k_nearest_neighbors(data, k):
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        
        # Calculate the Euclidean distance between each data point and all other data points
        distances = np.linalg.norm(df["valor"].values[:, np.newaxis] - df["valor"].values, axis=1)
        
        # Sort the distances in ascending order
        sorted_distances = np.sort(distances)
        
        # Get the k nearest neighbors
        nearest_neighbors = sorted_distances[:k]
        
        # Calculate the anomaly threshold as the mean plus three times the standard deviation of the nearest neighbors
        anomaly_threshold = np.mean(nearest_neighbors) + 3 * np.std(nearest_neighbors)
        
        # Identify the anomalies that exceed the anomaly threshold
        anomalies = df[df["valor"] > anomaly_threshold]["valor"].tolist()
        
        return anomalies
    @staticmethod
    def perform_pca(data):
        # Convert data to a DataFrame
        df = pd.DataFrame(data)
        
        # Select the numerical features for PCA
        features = ["valor"]
        X = df[features]
        
        # Perform PCA
        pca = PCA(n_components=2)
        principal_components = pca.fit_transform(X)
        
        # Get the explained variance ratio
        explained_variance_ratio = pca.explained_variance_ratio_
        
        # Get the anomaly threshold as the mean plus three times the standard deviation of the principal components
        anomaly_threshold = np.mean(principal_components) + 3 * np.std(principal_components)
        
        # Identify the anomalies that exceed the anomaly threshold
        anomalies = df[np.linalg.norm(principal_components, axis=1) > anomaly_threshold]["valor"].tolist()
        
        return anomalies
    
    @staticmethod
    def monecarlo(datarecive):
        
        df=pd.DataFrame(datarecive)
        mean_valor = df["valor"].mean()
        std_valor = df["valor"].std()
        num_simulations = 1000
        umbral_fallo=mean_valor+3*std_valor
        simulated_data = np.random.normal(mean_valor, std_valor, num_simulations)
        probabilidad_fallo = np.mean(simulated_data > umbral_fallo)
        return probabilidad_fallo
    @staticmethod
    def calculate_poisson_probability(data):
        df = pd.DataFrame(data)
        mean = df["valor"].mean()
        threshold = 3 * mean
        num_anomalies = len(df[df["valor"] > threshold])
        num_total = len(df)
        probability = num_anomalies / num_total
        
        return probability
    
    
    
    
    
    
            
