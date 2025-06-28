# src/guardian_ai/data_processing/process_vulnerable_code.py

import json
import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List
from tqdm import tqdm

# --- Path Definitions ---
try:
    # This works when the script is run directly.
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
except NameError:
    # This provides a fallback for interactive environments.
    PROJECT_ROOT = Path('.').resolve()

RAW_VC_DIR = PROJECT_ROOT / "data" / "raw" / "vulnerable_code"
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

# --- Core Functions ---

def parse_vc_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Safely parses a single vulnerable code JSON file with robust error handling.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️ Warning: Could not read or parse {file_path}. Error: {e}")
        return None

    # Use .get() to prevent KeyErrors from missing or incomplete files
    vuln_details = data.get('vulnerability_details', {})
    code_snippets = data.get('code_snippets', {})

    # Validate that essential fields exist and are not empty
    required_fields = {
        'id': data.get('id'),
        'language': data.get('language'),
        'cwe_id': vuln_details.get('cwe_id'),
        'description': vuln_details.get('description'),
        'vulnerable_code': code_snippets.get('vulnerable_code'),
        'fixed_code': code_snippets.get('fixed_code')
    }

    if not all(required_fields.values()):
        print(f"⚠️ Warning: Skipping {file_path} due to missing essential fields.")
        return None
        
    return required_fields

def create_training_prompts(parsed_data: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Generates multiple instruction-following training examples from a single parsed VC file.
    """
    vc_id = parsed_data['id']
    lang = parsed_data['language']
    vuln_code = parsed_data['vulnerable_code']
    fixed_code = parsed_data['fixed_code']
    cwe = parsed_data['cwe_id']
    desc = parsed_data['description']
    
    training_samples = []

    # Task 1: Vulnerability Detection and Explanation
    prompt1 = f"Analyze the following {lang} code for security vulnerabilities. If you find one, state the CWE it relates to and provide a brief explanation.\n\n```\n{vuln_code}\n```"
    response1 = f"This code is vulnerable to {cwe}. {desc}"
    training_samples.append({
        'source_id': vc_id,
        'task_type': 'detection_explanation',
        'prompt': prompt1,
        'response': response1
    })

    # Task 2: Code Repair
    prompt2 = f"The following {lang} code is insecure. Provide the corrected, secure version.\n\n```\n{vuln_code}\n```"
    response2 = f"Here is the fixed version of the code:\n\n```\n{fixed_code}\n```"
    training_samples.append({
        'source_id': vc_id,
        'task_type': 'code_repair',
        'prompt': prompt2,
        'response': response2
    })
    
    # Task 3: Code Diff Analysis
    prompt3 = f"Explain the security fix applied between the 'Vulnerable Code' and 'Fixed Code' snippets in {lang}.\n\n# Vulnerable Code\n```\n{vuln_code}\n```\n\n# Fixed Code\n```\n{fixed_code}\n```"
    response3 = f"The fix addresses {cwe} by moving from an insecure pattern to a secure one. The original code was vulnerable because {desc}. The new code is more secure because it mitigates this risk."
    training_samples.append({
        'source_id': vc_id,
        'task_type': 'diff_analysis',
        'prompt': prompt3,
        'response': response3
    })

    return training_samples

def process_all_vulnerable_code():
    """
    Main orchestrator to process all raw VC files into a training-ready dataset.
    """
    print("--- Starting Vulnerable Code Processing Pipeline ---")
    
    if not RAW_VC_DIR.exists():
        raise FileNotFoundError(f"❌ Raw data directory not found at: {RAW_VC_DIR}")

    vc_files = list(RAW_VC_DIR.glob('VC-*.json'))
    if not vc_files:
        print("⚠️ Warning: No vulnerable code files ('VC-*.json') found. Halting.")
        return

    print(f"✅ Found {len(vc_files)} vulnerable code files to process.")
    
    all_training_samples = []
    for file_path in tqdm(vc_files, desc="Processing VC files"):
        parsed_data = parse_vc_file(file_path)
        if parsed_data:
            prompts = create_training_prompts(parsed_data)
            all_training_samples.extend(prompts)
    
    if not all_training_samples:
        print("❌ Error: No training samples were generated. Check raw data and parsing logic.")
        return

    print(f"✅ Generated {len(all_training_samples)} training samples from {len(vc_files)} source files.")
    
    # Convert to DataFrame and save as Parquet
    df = pd.DataFrame(all_training_samples)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = PROCESSED_DATA_DIR / "processed_vulnerable_code_dataset.parquet"
    
    try:
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print(f"🎉 Success! Processed vulnerable code dataset saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: Failed to save data to Parquet file. Reason: {e}")

if __name__ == "__main__":
    try:
        process_all_vulnerable_code()
    except Exception as e:
        print(f"\nAn unexpected error occurred in the main process: {e}")