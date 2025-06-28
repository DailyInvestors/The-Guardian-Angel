# src/guardian_ai/data_processing/cve_parser.py

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

def parse_cve_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Parses a single raw, enriched CVE JSON file into a flat, ML-ready dictionary.

    Args:
        file_path: The path to the JSON file for a single CVE.

    Returns:
        A dictionary containing flattened and processed features, or None if parsing fails.
    """
    try:
        with file_path.open('r', encoding='utf-8') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"⚠️ Warning: Could not read or parse {file_path}. Error: {e}")
        return None

    # Use .get() extensively to prevent KeyErrors from missing fields
    enrichment = data.get('guardian_enrichment', {})
    cvss_v3 = data.get('cvss_v3', {}) or {} # Ensure it's a dict even if null
    cwe_list = data.get('cwe', [])
    exploit_db = enrichment.get('exploit_db', {}).get('exploits', [])
    cisa_kev = enrichment.get('cisa_kev', {})
    mitre = enrichment.get('mitre_attack', {}).get('techniques', [])

    # --- Feature Engineering ---
    text_parts = [data.get('description')]
    if cisa_kev.get('description'):
        text_parts.append(f"CISA KEV Summary: {cisa_kev.get('description')}")
    for tech in mitre:
        text_parts.append(f"Related MITRE Technique: {tech.get('technique_name')} ({tech.get('technique_id')})")
    
    unified_text = " . ".join(filter(None, text_parts))

    flat_data = {
        'cve_id': data.get('id'),
        'published_date': data.get('published_date_utc'),
        'cvss_v3_base_score': cvss_v3.get('base_score'),
        'cvss_v3_severity': cvss_v3.get('severity'),
        'cwe_id': cwe_list[0].get('id') if cwe_list else None,
        
        # Engineered boolean features - highly valuable for ML
        'has_exploit_db_poc': len(exploit_db) > 0,
        'is_in_cisa_kev': cisa_kev.get('is_exploited', False),

        # Extracted lists of identifiers
        'exploit_db_ids': [e.get('edb_id') for e in exploit_db],
        'mitre_technique_ids': [t.get('technique_id') for t in mitre],
        
        # The unified text block for the LLM
        'unified_text': unified_text
    }

    return flat_data