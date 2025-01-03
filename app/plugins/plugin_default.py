import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import skew, kurtosis
import json

class Plugin:
    """
    Plugin to preprocess the dataset for feature extraction.
    """
    # Define the parameters for this plugin and their default values
    plugin_params = {
        'target_column': 'CLOSE',
        'time_horizon': 6,
        'std_dev_horizon': 12
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
        Generate a training signal dataset by extracting DATE_TIME and the target column,
        shifting the target column forward by the specified time horizon, and calculating
        the standard deviation over the last self.params['std_dev_horizon'] ticks.

        Args:
            data (pd.DataFrame): The input data to be processed.

        Returns:
            pd.DataFrame: The processed dataset with DATE_TIME, target column, and standard deviation.
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
        print(f"[DEBUG] Extracted columns: {list(processed_data.columns)}")

        # Step 3: Shift the target column forward by time_horizon ticks
        time_horizon = self.params['time_horizon']
        print(f"[DEBUG] Shifting target column '{target_column}' forward by {time_horizon} ticks...")

        processed_data[target_column] = processed_data[target_column].shift(-time_horizon)

        # Step 4: Calculate the rolling standard deviation
        std_dev_horizon = self.params['std_dev_horizon']
        print(f"[DEBUG] Calculating rolling standard deviation over the last {std_dev_horizon} ticks...")

        processed_data['std_dev'] = processed_data[target_column].rolling(window=std_dev_horizon).std()

        # Step 5: Drop rows with NaN values (from both shift and rolling calculations)
        initial_shape = processed_data.shape
        processed_data.dropna(inplace=True)
        final_shape = processed_data.shape
        print(f"[DEBUG] Processed data shape before dropping NaN: {initial_shape}")
        print(f"[DEBUG] Processed data shape after dropping NaN: {final_shape}")

        # Step 6: Reset index if necessary
        processed_data.reset_index(drop=True, inplace=True)

        # Optional: Sort by DATE_TIME to ensure chronological order
        processed_data.sort_values(by='DATE_TIME', inplace=True)
        processed_data.reset_index(drop=True, inplace=True)

        print(f"[DEBUG] Final processed data shape: {processed_data.shape}")
        return processed_data


# Example usage
if __name__ == "__main__":
    plugin = Plugin()
    data = pd.read_csv('tests/data/EURUSD_5m_2010_2015.csv', header=None)
    print(f"Loaded data shape: {data.shape}")
    processed_data = plugin.process(data)
    print(processed_data)
