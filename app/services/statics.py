import pandas as pd 
import matplotlib.pyplot as plt


class DataStatictsService:
    @staticmethod
    def meditions(data):
        # Separate data by sensor type
        sensor_data = {}
        for item in data:
            sensor_type = item['nameSensor']
            if sensor_type not in sensor_data:
                sensor_data[sensor_type] = []
            sensor_data[sensor_type].append(item['valor'])
        
        # Process data for each sensor type
        results = {}
        
        for sensor_type, values in sensor_data.items():
           
            results[sensor_type] = {
                'median': float(pd.Series(values).median()),
                'mode': float(pd.Series(values).mode().values[0]),
                'mean': float(pd.Series(values).mean()),
                'std': float(pd.Series(values).std())
            }
        
        return results