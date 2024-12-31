
# Training-Signal

The **Training-Signal** project is a flexible and modular application designed for generating training signals from time series data. It supports dynamic loading of plugins for various preprocessing tasks. Currently, the only available plugin is the default plugin, which extracts and shifts target columns to create training signals. Each plugin can save and load its parameters to ensure consistent processing across different datasets.

## Table of Contents

- [Installation Instructions](#installation-instructions)
- [Usage Examples](#usage-examples)
  - [Default Plugin for Generating Training Signals](#default-plugin-for-generating-training-signals)
- [Configuration Parameters](#configuration-parameters)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Installation Instructions

To install and set up the Training-Signal application, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/harveybc/trading-signal.git
    cd trading-signal
    ```

2. **Create and Activate a Virtual Environment**:
    - **Using `venv` (Python 3.3+)**:
        ```bash
        python -m venv env
        source env/bin/activate  # On Windows use `env\Scripts\activate`
        ```

    - **Using `conda`**:
        ```bash
        conda create --name trading-signal_env python=3.9
        conda activate trading-signal_env
        ```

3. **Install Dependencies**:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

4. **Build the Package**:
    ```bash
    python -m build
    ```

5. **Install the Package**:
    ```bash
    pip install .
    ```

6. **Run the Training-Signal Application**:
    - On Windows, run the following command to verify installation (it uses all default values; use `trading-signal.bat --help` for complete command line arguments description):
        ```bash
        trading-signal.bat
        ```

    - On Linux, run:
        ```bash
        sh trading-signal.sh
        ```

7. **Run Tests (Optional, requires external repo)**:
    For passing remote tests, an instance of [harveybc/data-logger](https://github.com/harveybc/data-logger) is required.
    - On Windows, run the following command to run the tests:
        ```bash
        set_env.bat
        pytest
        ```

    - On Linux, run:
        ```bash
        sh ./set_env.sh
        pytest
        ```

8. **Generate Documentation (Optional)**:
    - Run the following command to generate code documentation in HTML format in the `docs` directory:
        ```bash
        pdoc --html -o docs app
        ```

This command should display the help message for the Training-Signal application, confirming that the installation was successful.

## Usage Examples

You can use the Training-Signal application from the command line with various plugins. Below is an example:

### Default Plugin for Generating Training Signals

The **Default Plugin** processes the input dataset to create a training signal by extracting the `DATE_TIME` and a specified target column. It shifts the target values forward by a defined time horizon to generate the training labels.

#### Example Command

```bash
trading-signal.bat --plugin default --target_column CLOSE --time_horizon 5 --input_file data/input.csv --output_file data/training_signal.csv
```

#### Parameters:

- `--plugin`: Specifies the plugin to use. For generating training signals, use `default`.
- `--target_column`: The name of the target column to extract and shift (e.g., `CLOSE`).
- `--time_horizon`: The number of ticks to shift the target column forward (e.g., `5`).
- `--input_file`: Path to the input CSV file containing the dataset.
- `--output_file`: Path where the generated training signal CSV will be saved.

## Configuration Parameters

The Training-Signal application and its plugins can be configured using command-line arguments. Below are some common parameters:

- **General Parameters**:
  - `--input_file`: Path to the input CSV file.
  - `--output_file`: Path to the output CSV file.
  - `--quiet_mode`: Suppresses non-error messages when set to `true`.
  - `--force_date`: Ensures the `DATE_TIME` column is included in the output if set to `true`.
  - `--headers`: Includes headers in the output CSV if set to `true`.

- **Plugin-Specific Parameters**:
  - **Default Plugin**:
    - `--plugin`: `default`
    - `--target_column`: Name of the target column to extract (e.g., `CLOSE`).
    - `--time_horizon`: Number of ticks to shift the target column forward (e.g., `5`).

Use the `-h` or `--help` parameter to get detailed information on all available parameters:

```bash
trading-signal.bat --help
```

## File Structure

The current file structure of the Training-Signal project is as follows:

```markdown
trading-signal/
│
├── config_out.json         # Example configuration output file for debugging
├── dataset_analyzer.py     # Analyzes and provides insights into datasets
├── debug_out.json          # Example debug output file
├── LICENSE.txt             # Project license file (MIT License)
├── pyproject.toml          # Build system configuration
├── README.md               # Project readme file
├── requirements.txt        # Required Python packages
├── setup.py                # Script to set up and install the package
├── set_env.bat             # Windows batch script for environment setup
├── set_env.sh              # Linux shell script for environment setup
├── app/                    # Main application package
│   ├── cli.py              # Command-line interface logic
│   ├── config.py           # Application configuration file
│   ├── config_handler.py   # Handles configuration parsing and validation
│   ├── config_merger.py    # Merges multiple configuration sources
│   ├── data_handler.py     # Handles data loading and processing
│   ├── data_processor.py   # Core data processing pipeline logic
│   ├── main.py             # Application entry point
│   └── plugins/            # Plugins for extending functionality
│       └── plugin_default.py # Default plugin for generating training signals
├── tests/                  # Unit, system, integration, and user tests
│   ├── conftest.py         # Test configuration file for pytest
│   ├── data/               # Directory for test datasets
│   ├── integration_tests/  # Integration test cases
│   ├── system_tests/       # System-level test cases
│   ├── unit_tests/         # Unit test cases for individual modules
│   └── user_tests/         # User acceptance test cases
├── trading-signal.bat      # Windows batch script to run the application
└── trading-signal.sh       # Linux shell script to run the application
```

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**:
    ```bash
    git checkout -b feature/YourFeatureName
    ```
3. **Commit Your Changes**:
    ```bash
    git commit -m "Add Your Feature"
    ```
4. **Push to the Branch**:
    ```bash
    git push origin feature/YourFeatureName
    ```
5. **Open a Pull Request**

Please ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the [MIT License](LICENSE).

---

## Important Notes

- **Configuration Parameters**: Ensure that the `self.params` dictionary within your plugin includes the keys `'target_column'` and `'time_horizon'` with appropriate values. For example:

  ```python
  self.params = {
      'target_column': 'CLOSE',  # Replace with your actual target column name
      'time_horizon': 5,         # Replace with the desired number of ticks
      # ... other parameters
  }
  ```

- **Input Data Requirements**: The input CSV must contain the `DATE_TIME` column and the specified `target_column`. The `DATE_TIME` column should be in a datetime format recognizable by Pandas.

- **Output Handling**: The `run_processing_pipeline` function will write the processed (shifted) data to the specified `output_file`. Ensure that the output path is correctly set in your configuration.

- **Error Handling**: The updated `process` method includes error checks to ensure that necessary columns are present. Make sure to handle these exceptions appropriately in your broader application context.

- **Testing**: Before deploying the updated plugin in a production environment, it's advisable to perform thorough testing with various datasets to ensure that the shifting behaves as expected and that no edge cases are overlooked.

By following the updated instructions and utilizing the default plugin, you can effectively generate robust training signals for your machine learning projects.
