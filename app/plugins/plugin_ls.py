import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
import json

class Plugin:
    """
    Plugin to preprocess the dataset for traainign NEAT agent including hourly and daily predictions, rolling standard deviations, and proper column organization.
    """
    # Define the parameters for this plugin and their default values
    plugin_params = {
        'target_column': 'CLOSE',
        'time_horizon': 6,
        'std_dev_horizon': 12,
        'daily_horizon': 6

    }

    # Define the debug variables for this plugin
    plugin_debug_vars = ['column_metrics', 'normalization_params']

    def __init__(self):
        """
        Initialize the Plugin with default parameters.
        """
        self.params = self.plugin_params.copy()
        self.normalization_params = {}  # To store normalization parameters for each column
        self.column_metrics = {}  # To store metrics for each column

    def set_params(self, **kwargs):
        """
        Set the parameters for the plugin.

        Args:
            **kwargs: Arbitrary keyword arguments for plugin parameters.
        """
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value

    def get_debug_info(self):
        """
        Get debug information for the plugin.

        Returns:
            dict: Debug information including column metrics and normalization parameters.
        """
        debug_info = {
            'column_metrics': self.column_metrics,
            'normalization_params': self.normalization_params
        }
        return debug_info

    def add_debug_info(self, debug_info):
        """
        Add debug information to the given dictionary.

        Args:
            debug_info (dict): The dictionary to add debug information to.
        """
        debug_info.update(self.get_debug_info())

    def process(self, data):
        """
        Generate a training signal dataset with predictions for hourly and daily horizons,
        rolling standard deviations, and proper column organization.

        Args:
            data (pd.DataFrame): The input data to be processed.

        Returns:
            pd.DataFrame: The processed dataset ready for NEAT.
        """
        print(f"[DEBUG] Loaded data shape: {data.shape}")
        print(f"[DEBUG] Columns in the data: {list(data.columns)}")

        # Paso 1: Asegurarse de que la columna DATE_TIME esté como columna regular
        if isinstance(data.index, pd.DatetimeIndex):
            print("[DEBUG] DATE_TIME está actualmente como índice. Reiniciando a columna regular...")
            data.reset_index(inplace=True)
        if 'DATE_TIME' not in data.columns:
            raise ValueError("[ERROR] La columna DATE_TIME falta en los datos de entrada!")

        # Paso 2: Extraer DATE_TIME y la columna objetivo
        target_column = self.params['target_column']
        print(f"[DEBUG] Target column: {target_column}")

        if target_column not in data.columns:
            raise ValueError(f"[ERROR] La columna objetivo '{target_column}' falta en los datos de entrada!")

        # Extraer columnas relevantes
        processed_data = data[['DATE_TIME', target_column]].copy()

        # Paso 3: Generar predicciones horarias (horizonte a corto plazo)
        time_horizon = self.params['time_horizon']
        print(f"[DEBUG] Generando predicciones horarias para los próximos {time_horizon} ticks...")
        for i in range(1, time_horizon + 1):
            processed_data[f"{target_column}_t+{i}"] = processed_data[target_column].shift(-i)

        # Paso 4: Generar predicciones diarias (horizonte a largo plazo)
        print("[DEBUG] Calculando daily HIGH, LOW, CLOSE, OPEN...")
        data['DATE'] = pd.to_datetime(data['DATE_TIME']).dt.date  # Extraer fecha
        daily_data = data.groupby('DATE')[target_column].agg(
            HIGH='max',
            LOW='min',
            CLOSE='last',
            OPEN='first'
        ).reset_index()

        # Renombrar columnas diarias para evitar conflictos durante la fusión
        daily_data = daily_data.rename(columns={
            'HIGH': 'daily_HIGH',
            'LOW': 'daily_LOW',
            'CLOSE': 'daily_CLOSE',
            'OPEN': 'daily_OPEN'
        })

        daily_horizon = self.params['daily_horizon']
        print(f"[DEBUG] Generando predicciones diarias para los próximos {daily_horizon} días...")
        for col in ['daily_HIGH', 'daily_LOW', 'daily_CLOSE', 'daily_OPEN']:
            for i in range(1, daily_horizon + 1):
                daily_data[f"{col}_D{i}"] = daily_data[col].shift(-i)

        # Fusión de las predicciones diarias de vuelta al conjunto de datos principal
        processed_data['DATE'] = pd.to_datetime(processed_data['DATE_TIME']).dt.date
        processed_data = processed_data.merge(daily_data, on='DATE', how='left')

        # Paso 5: Calcular desviaciones estándar móviles
        std_dev_horizon = self.params['std_dev_horizon']
        print(f"[DEBUG] Calculando desviación estándar móvil sobre los últimos {std_dev_horizon} ticks...")
        if target_column not in processed_data.columns:
            raise KeyError(f"La columna objetivo '{target_column}' no se encontró después de la fusión.")
        processed_data['std_dev_12h'] = processed_data[target_column].rolling(window=std_dev_horizon).std()

        print("[DEBUG] Calculando desviación estándar móvil sobre los últimos 12 días...")
        processed_data['std_dev_12d'] = processed_data[target_column].rolling(window=12 * 24).std()

        # Paso 6: Eliminar filas con valores NaN
        initial_shape = processed_data.shape
        processed_data.dropna(inplace=True)
        final_shape = processed_data.shape
        print(f"[DEBUG] Forma de los datos procesados antes de eliminar NaN: {initial_shape}")
        print(f"[DEBUG] Forma de los datos procesados después de eliminar NaN: {final_shape}")

        # Paso 7: Organizar columnas según la estructura acordada
        print("[DEBUG] Organizando columnas...")
        hourly_columns = [f"{target_column}_t+{i}" for i in range(1, time_horizon + 1)]
        daily_columns = [f"{col}_D{i}" for col in ['daily_HIGH', 'daily_LOW', 'daily_CLOSE', 'daily_OPEN'] for i in range(1, daily_horizon + 1)]
        std_dev_columns = ['std_dev_12h', 'std_dev_12d']

        final_columns = ['DATE_TIME'] + hourly_columns + daily_columns + std_dev_columns
        processed_data = processed_data[final_columns]

        print(f"[DEBUG] Forma final de los datos procesados: {processed_data.shape}")
        return processed_data




# Example usage
if __name__ == "__main__":
    plugin = Plugin()
    data = pd.read_csv('tests/data/EURUSD_5m_2010_2015.csv', header=None)
    print(f"Loaded data shape: {data.shape}")
    processed_data = plugin.process(data)
    print(processed_data)
