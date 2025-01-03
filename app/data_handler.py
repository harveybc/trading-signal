import pandas as pd


def load_csv(file_path):
    """
    Load a CSV file assuming it has headers and a 'DATE_TIME' column at the beginning.
    The 'DATE_TIME' column remains as a regular column, and all other columns are converted to numeric.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded and processed DataFrame.
    """
    try:
        # Leer el CSV con encabezados y parsear la primera columna como fechas
        data = pd.read_csv(file_path, sep=',', parse_dates=[0], dayfirst=True)

        # Renombrar explícitamente la primera columna a 'DATE_TIME'
        data.rename(columns={data.columns[0]: 'DATE_TIME'}, inplace=True)

        print(f"[DEBUG] Loaded data columns: {list(data.columns)}")  # Línea de depuración

        # Convertir todas las columnas excepto 'DATE_TIME' a numéricas, coercionando errores a NaN
        for col in data.columns:
            if col != 'DATE_TIME':
                data[col] = pd.to_numeric(data[col], errors='coerce')

        # Validar la existencia de la columna 'CLOSE'
        if 'CLOSE' not in data.columns:
            raise KeyError("La columna 'CLOSE' falta en los datos de entrada!")

        # Manejar valores NaN en la columna 'CLOSE'
        if data['CLOSE'].isna().any():
            print("[WARNING] La columna 'CLOSE' contiene valores NaN. Rellenando valores faltantes...")
            data['CLOSE'].fillna(method='ffill', inplace=True)  # Relleno hacia adelante
            data['CLOSE'].fillna(method='bfill', inplace=True)  # Relleno hacia atrás si es necesario

        print(f"[DEBUG] First 5 rows of the data:\n{data.head()}")  # Línea de depuración

    except Exception as e:
        print(f"[ERROR] Ocurrió un error al cargar el CSV: {e}")
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
