import pandas as pd 
import matplotlib.pyplot as plt

class DataProcessingService:
    @staticmethod
    def process_sensor_data(sensor_values):
        # Procesar los datos del sensor en pandas
        
        df = pd.DataFrame(sensor_values, columns=["valor"])
        
        # Calcular histograma
        frequencies, bins, _ = plt.hist(df["valor"], bins=10)
        
        # Obtener los valores de los bins
        values = bins[:-1]
        
        # Crear un array de valores para el histograma
        histogram_data = [{"value": value, "frequency": frequency} for value, frequency in zip(values, frequencies)]
        # Obtener las frecuencias del histograma
        frequencies = [data["frequency"] for data in histogram_data]

        # Obtener los valores del histograma
        values = [data["value"] for data in histogram_data]

        # Devolver los arreglos de frecuencias y valores
        return frequencies, values
        
       
    @staticmethod
    
    def process_sensor_data_probabilistic(sensor_data1, sensor_data2):
        # Obtener los valores de los sensores
        values1 = [data["valor"] for data in sensor_data1]
        values2 = [data["valor"] for data in sensor_data2]
        sensorone = sensor_data1[0]["nameSensor"]
        sensortwo = sensor_data2[0]["nameSensor"]

        # Obtener la longitud mínima de los arrays
        min_length = min(len(values1), len(values2))

        # Crear un DataFrame de pandas con los valores de los sensores
        df = pd.DataFrame({sensorone: values1[:min_length], sensortwo: values2[:min_length]})

        # Calcular la probabilidad conjunta de los valores de los sensores
        joint_prob = df.groupby([sensorone, sensortwo]).size().reset_index(name="Frequency")

        # Crear un array de valores para el scatter plot
        scatter_data = [{"x": row[sensorone], "y": row[sensortwo], "frequency": row["Frequency"]} for _, row in joint_prob.iterrows()]
        
        return scatter_data
    @staticmethod
    def linechart(sensor_data):
       df = pd.DataFrame(sensor_data)

    # Convertir createdAt a formato datetime
       df['createdAt'] = pd.to_datetime(df['createdAt'])

    # Extraer mes y año para agrupar
       df['month_year'] = df['createdAt'].dt.to_period('M')

    # Agrupar datos por sensor y mes/año
       grouped = df.groupby(['nameSensor', 'month_year']).agg({'valor': 'mean'}).reset_index()

    # Ordenar los meses de menor a mayor
       grouped.sort_values(by='month_year', inplace=True)

    # Convertir el periodo de vuelta a una cadena
       grouped['month_year'] = grouped['month_year'].astype(str)

    # Crear la estructura para Chart.js
       result = {}
       result['labels'] = grouped['month_year'].unique().tolist()

       sensors = grouped['nameSensor'].unique()
       for sensor in sensors:
            sensor_data = grouped[grouped['nameSensor'] == sensor]
            result[sensor] = sensor_data['valor'].fillna(0).tolist()

       return result
    
    @staticmethod
    def frequency_table(data):
        df = pd.DataFrame(data)
    
    # Crear tabla de frecuencias para cada sensor
        frequency_tables = {}
        sensors = df['nameSensor'].unique()
    
        for sensor in sensors:
            sensor_data = df[df['nameSensor'] == sensor]
            freq_table = sensor_data['valor'].value_counts().reset_index()
            freq_table.columns = ['valor', 'frecuencia']
            frequency_tables[sensor] = freq_table.to_dict(orient='records')
    
        return frequency_tables
      
    @staticmethod
    def boxplot(data):
      df = pd.DataFrame(data)

      # Crear un DataFrame separado para cada sensor
      sensor_dfs = {}
      sensors = df['nameSensor'].unique()

      for sensor in sensors:
         sensor_data = df[df['nameSensor'] == sensor]
         sensor_dfs[sensor] = sensor_data['valor']

      # Crear una lista de listas con los valores de cada sensor
      boxplot_data = [sensor_dfs[sensor].tolist() for sensor in sensors]

      # Crear la estructura para Chart.js
      result = {}
      result['labels'] = sensors.tolist()
      result['datasets'] = [{'label': sensor, 'data': values} for sensor, values in zip(sensors, boxplot_data)]

      return result

   

     
    
    



    


    
    