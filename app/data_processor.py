from app.data_handler import load_csv, write_csv


def run_processing_pipeline(config, plugin):
    """Process the data using the specified plugin."""
    data = load_csv(config['input_file'])

    # Debugging: Print loaded data
    print("Loaded data:\n", data.head())

    processed_data = plugin.process(data)

    # Debugging: Print processed data
    print("Processed data:\n", processed_data.head())

    include_date = config['force_date'] if 'date' in processed_data.columns else False

    if not config['quiet_mode']:
        print("Processing complete. Writing output...")

    # Write separate file for short-term (hourly) predictions
    hourly_cols = [col for col in processed_data.columns if col.startswith("Prediction_h_")]
    if "DATE_TIME" in processed_data.columns:
        hourly_cols = ["DATE_TIME"] + hourly_cols
    write_csv(config['hourly_output_file'], processed_data[hourly_cols], include_date=include_date, headers=config['headers'])
    if not config['quiet_mode']:
        print(f"Hourly predictions output written to {config['hourly_output_file']}")

    # Write separate file for long-term (daily) predictions
    daily_cols = [col for col in processed_data.columns if col.startswith("Prediction_d_")]
    if "DATE_TIME" in processed_data.columns:
        daily_cols = ["DATE_TIME"] + daily_cols
    write_csv(config['daily_output_file'], processed_data[daily_cols], include_date=include_date, headers=config['headers'])
    if not config['quiet_mode']:
        print(f"Daily predictions output written to {config['daily_output_file']}")

    return processed_data

