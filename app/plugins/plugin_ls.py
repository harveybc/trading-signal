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

        # Step 1: Ensure DATE_TIME column is included as a regular column
        if isinstance(data.index, pd.DatetimeIndex):
            print("[DEBUG] DATE_TIME is currently the index. Resetting it to a regular column...")
            data.reset_index(inplace=True)
        if 'DATE_TIME' not in data.columns:
            raise ValueError("[ERROR] DATE_TIME column is missing in the input data!")

        # Step 2: Extract DATE_TIME and target column
        target_column = self.params['target_column']
        print(f"[DEBUG] Target column: {target_column}")

        if target_column not in data.columns:
            raise ValueError(f"[ERROR] Target column '{target_column}' is missing in the input data!")

        # Extract relevant columns
        processed_data = data[['DATE_TIME', target_column]].copy()

        # Step 3: Generate hourly predictions (short-term horizon)
        time_horizon = self.params['time_horizon']
        print(f"[DEBUG] Generating hourly predictions for the next {time_horizon} ticks...")
        for i in range(1, time_horizon + 1):
            processed_data[f"{target_column}_t+{i}"] = processed_data[target_column].shift(-i)

        # Step 4: Generate daily predictions (long-term horizon)
        print("[DEBUG] Calculating daily HIGH, LOW, CLOSE, OPEN...")
        data['DATE'] = pd.to_datetime(data['DATE_TIME']).dt.date  # Extract date
        daily_data = data.groupby('DATE')[target_column].agg(
            HIGH='max',
            LOW='min',
            CLOSE='last',
            OPEN='first'
        ).reset_index()

        daily_horizon = self.params['daily_horizon']
        print(f"[DEBUG] Generating daily predictions for the next {daily_horizon} days...")
        for col in ['HIGH', 'LOW', 'CLOSE', 'OPEN']:
            for i in range(1, daily_horizon + 1):
                daily_data[f"{col}_D{i}"] = daily_data[col].shift(-i)

        # Merge daily predictions back to the main dataset
        processed_data['DATE'] = pd.to_datetime(processed_data['DATE_TIME']).dt.date
        processed_data = processed_data.merge(daily_data, on='DATE', how='left')

        # Step 5: Calculate rolling standard deviations
        std_dev_horizon = self.params['std_dev_horizon']
        print(f"[DEBUG] Calculating rolling standard deviation over the last {std_dev_horizon} ticks...")
        processed_data['std_dev_12h'] = processed_data[target_column].rolling(window=std_dev_horizon).std()

        print("[DEBUG] Calculating rolling standard deviation over the last 12 days...")
        processed_data['std_dev_12d'] = data[target_column].rolling(window=12 * 24).std()

        # Step 6: Drop rows with NaN values
        initial_shape = processed_data.shape
        processed_data.dropna(inplace=True)
        final_shape = processed_data.shape
        print(f"[DEBUG] Processed data shape before dropping NaN: {initial_shape}")
        print(f"[DEBUG] Processed data shape after dropping NaN: {final_shape}")

        # Step 7: Organize columns as per agreed structure
        print("[DEBUG] Organizing columns...")
        hourly_columns = [f"{target_column}_t+{i}" for i in range(1, time_horizon + 1)]
        daily_columns = [f"{col}_D{i}" for col in ['HIGH', 'LOW', 'CLOSE', 'OPEN'] for i in range(1, daily_horizon + 1)]
        std_dev_columns = ['std_dev_12h', 'std_dev_12d']

        final_columns = ['DATE_TIME'] + hourly_columns + daily_columns + std_dev_columns
        processed_data = processed_data[final_columns]

        print(f"[DEBUG] Final processed data shape: {processed_data.shape}")
        return processed_data




# Example usage
if __name__ == "__main__":
    plugin = Plugin()
    data = pd.read_csv('tests/data/EURUSD_5m_2010_2015.csv', header=None)
    print(f"Loaded data shape: {data.shape}")
    processed_data = plugin.process(data)
    print(processed_data)
