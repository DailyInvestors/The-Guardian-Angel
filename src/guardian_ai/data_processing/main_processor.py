# src/guardian_ai/data_processing/main_processor.py

import pandas as pd
from pathlib import Path
from tqdm import tqdm
from cve_parser import parse_cve_file

# Define project paths relative to this script's location.
# This makes the script robust and runnable from anywhere.
try:
    # This works when the script is run directly.
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
except NameError:
    # This provides a fallback for interactive environments (like Jupyter).
    PROJECT_ROOT = Path('.').resolve()

RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw" / "cve_details"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

def process_all_cves():
    """
    Finds all raw CVE JSON files, processes them using the cve_parser,
    and saves the consolidated data as an efficient Parquet file.
    """
    print("--- Starting GuardianAI Data Processing Pipeline ---")
    
    # 1. Input Validation
    if not RAW_DATA_DIR.exists():
        raise FileNotFoundError(
            f"❌ Raw data directory not found. "
            f"Expected it at: {RAW_DATA_DIR}"
        )

    # 2. File Discovery
    cve_files = list(RAW_DATA_DIR.glob('CVE-*.json'))
    if not cve_files:
        print("⚠️ Warning: No CVE JSON files found in the raw data directory. Halting.")
        return

    print(f"✅ Found {len(cve_files)} CVE files to process.")
    
    # 3. Data Parsing and Aggregation
    all_processed_data = []
    # Use tqdm for a nice progress bar during processing.
    for file_path in tqdm(cve_files, desc="Parsing CVE files"):
        processed_data = parse_cve_file(file_path)
        if processed_data:
            all_processed_data.append(processed_data)

    # 4. Post-processing Validation
    if not all_processed_data:
        print("❌ Error: No data was successfully processed. Halting.")
        return

    print(f"✅ Successfully parsed {len(all_processed_data)} CVEs.")
    
    # 5. Data Conversion and Saving
    # Convert the list of dictionaries to a Pandas DataFrame for easy handling.
    df = pd.DataFrame(all_processed_data)
    
    # Ensure the output directory exists.
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "processed_cve_dataset.parquet"
    
    try:
        # Save to Parquet format, which is efficient for storage and reading.
        # We use the pyarrow engine and don't save the pandas index.
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"🎉 Success! Processed data saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: Failed to save data to Parquet file. Reason: {e}")

if __name__ == "__main__":
    try:
        process_all_cves()
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred during the main processing run: {e}")