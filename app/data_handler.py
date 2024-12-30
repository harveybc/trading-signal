import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file assuming it has headers and a 'DATE_TIME' column at the beginning.
    The 'DATE_TIME' column remains as a regular column.
    """
    try:
        # Read CSV with headers and parse the first column (assumed to be the 'DATE_TIME' column)
        data = pd.read_csv(file_path, sep=',', parse_dates=[0], dayfirst=True)

        # Explicitly ensure the first column is named 'DATE_TIME'
        data.rename(columns={data.columns[0]: 'DATE_TIME'}, inplace=True)

        print(f"[DEBUG] Loaded data columns: {data.columns}")  # Debugging line

        # Convert all non-'DATE_TIME' columns to numeric, coercing errors to NaN
        for col in data.columns:
            if col != 'DATE_TIME':
                data[col] = pd.to_numeric(data[col], errors='coerce')

        print(f"[DEBUG] First 5 rows of the data:\n{data.head()}")

    except Exception as e:
        print(f"[ERROR] An error occurred while loading the CSV: {e}")
        raise

    return data





def write_csv(file_path, data, include_date=True, headers=True):
    """
    Write a DataFrame to a CSV file, optionally including the date column and headers.
    
    Parameters:
    - file_path: str: Path to the output CSV file
    - data: pd.DataFrame: DataFrame to save
    - include_date: bool: Whether to include the 'date' column in the output
    - headers: bool: Whether to include the column headers in the output
    """
    try:
        if include_date and 'date' in data.columns:
            data.to_csv(file_path, index=True, header=headers)
        else:
            data.to_csv(file_path, index=False, header=headers)
    except Exception as e:
        print(f"An error occurred while writing the CSV: {e}")
        raise
