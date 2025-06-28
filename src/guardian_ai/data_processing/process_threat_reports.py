# src/guardian_ai/data_processing/process_threat_reports.py

import re
import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from typing import Dict, Any, Optional

# --- Configuration ---
# In a real project, we might use a pre-trained NER model for actors/malware.
# For simplicity here, we'll use regex and keyword lists.
KNOWN_ACTORS = ['unc2452', 'lapsus$', 'apt29', 'cozy bear']
KNOWN_MALWARE = ['sunburst', 'teardrop', 'darkme', 'guloader', 'remcos rat']

# Regex to find common IOCs and entities
REGEX_PATTERNS = {
    'cves': r'(CVE-\d{4}-\d{4,7})',
    'mitre_techniques': r'(T\d{4}(\.\d{3})?)',
    'ipv4': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    'domains': r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}',
    'md5': r'\b[a-fA-F0-9]{32}\b',
    'sha1': r'\b[a-fA-F0-9]{40}\b',
    'sha256': r'\b[a-fA-F0-9]{64}\b',
}

# --- Path Definitions ---
try:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
except NameError:
    PROJECT_ROOT = Path('.').resolve()

RAW_TR_DIR = PROJECT_ROOT / "data" / "raw" / "threat_reports"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

def extract_entities_from_text(text: str) -> Dict[str, Any]:
    """
    Uses regex and keyword matching to extract structured entities from raw text.
    """
    entities = {key: [] for key in REGEX_PATTERNS}
    entities['actors'] = []
    entities['malware'] = []
    
    text_lower = text.lower()
    
    # Extract using regex
    for key, pattern in REGEX_PATTERNS.items():
        # Use set to get unique matches
        matches = set(re.findall(pattern, text_lower, re.IGNORECASE))
        # For MITRE techniques, we only want the primary ID (TXXXX)
        if key == 'mitre_techniques':
             entities[key] = sorted([m[0] if isinstance(m, tuple) else m for m in matches])
        else:
             entities[key] = sorted(list(matches))

    # Extract using keyword lists
    for actor in KNOWN_ACTORS:
        if re.search(r'\b' + actor + r'\b', text_lower):
            entities['actors'].append(actor.replace('$', '')) # Clean up regex chars
    
    for malware in KNOWN_MALWARE:
        if re.search(r'\b' + malware + r'\b', text_lower):
            entities['malware'].append(malware)

    # Consolidate IOCs
    iocs = []
    for ioc_type in ['ipv4', 'domains', 'md5', 'sha1', 'sha256']:
        for value in entities.pop(ioc_type, []):
            iocs.append({'type': ioc_type, 'value': value})
    
    entities['iocs'] = iocs
    return entities

def process_single_report(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Processes a single threat report file, extracting metadata and entities.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            full_text = f.read()
    except Exception as e:
        print(f"⚠️ Warning: Could not read {file_path}. Error: {e}")
        return None
        
    if not full_text.strip():
        return None

    # Basic metadata extraction (can be improved)
    title_match = re.search(r'Title:\s*(.*)', full_text)
    source_match = re.search(r'Source:\s*(.*)', full_text)
    date_match = re.search(r'Date:\s*(\d{4}-\d{2}-\d{2})', full_text)

    # Extract structured data
    entities = extract_entities_from_text(full_text)
    
    processed_data = {
        'source_file': file_path.name,
        'title': title_match.group(1).strip() if title_match else None,
        'source_name': source_match.group(1).strip() if source_match else None,
        'publication_date': date_match.group(1).strip() if date_match else None,
        'full_text': full_text,
        'summary': "", # Placeholder: a real pipeline would use a summarization model
        **entities # Unpack all extracted entities into the main dictionary
    }
    return processed_data


def process_all_threat_reports():
    """Main orchestrator to process all raw threat report files."""
    print("--- Starting Threat Report Processing Pipeline ---")
    
    if not RAW_TR_DIR.exists():
        raise FileNotFoundError(f"❌ Raw data directory not found at: {RAW_TR_DIR}")

    tr_files = list(RAW_TR_DIR.glob('TR-*.txt'))
    if not tr_files:
        print("⚠️ Warning: No threat report files ('TR-*.txt') found. Halting.")
        return

    print(f"✅ Found {len(tr_files)} threat report files to process.")
    
    all_processed_reports = []
    for file_path in tqdm(tr_files, desc="Processing Reports"):
        processed_data = process_single_report(file_path)
        if processed_data:
            all_processed_reports.append(processed_data)
            
    if not all_processed_reports:
        print("❌ Error: No reports were successfully processed.")
        return
        
    print(f"✅ Generated structured data for {len(all_processed_reports)} reports.")
    
    # Convert to DataFrame and save
    df = pd.DataFrame(all_processed_reports)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "processed_threat_reports_dataset.parquet"
    
    try:
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"🎉 Success! Processed threat report dataset saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: Failed to save data to Parquet file. Reason: {e}")


if __name__ == "__main__":
    # NOTE: To use a real summarization/NER model, you would initialize it here
    # and pass it to the processing functions. For now, this is self-contained.
    process_all_threat_reports()