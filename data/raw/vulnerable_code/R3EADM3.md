/data/raw/
└── vulnerable_code/
    ├── README.md               # VERY IMPORTANT: Explains the schema and how to contribute.
    ├── VC-00001_py_sqli.json   # Example: Python SQL Injection
    ├── VC-00002_java_patht.json# Example: Java Path Traversal
    ├── VC-00003_js_xss.json    # Example: JavaScript XSS
    ├── VC-00004_cpp_bo.json    # Example: C++ Buffer Overflow
    └── ...                     # Hundreds or thousands more files



// Template for a vulnerable code JSON file.
{
  "id": "VC-XXXXX", // Unique identifier for this code sample.
  "language": "python | java | javascript | csharp | c++ | etc.",
  "source_info": {
    "type": "GitHub Commit | CVE Report | CTF Challenge | Manual Example",
    "url": "URL to the source commit, report, or challenge",
    "related_cve": "CVE-XXXX-XXXX" // Optional: Links back to our CVE data.
  },
  "vulnerability_details": {
    "cwe_id": "CWE-XX", // e.g., "CWE-89" for SQL Injection
    "cwe_name": "Name of the Common Weakness Enumeration", // e.g., "SQL Injection"
    "description": "A clear, natural language explanation of why the code is vulnerable. This is crucial for the LLM."
  },
  "code_snippets": {
    "vulnerable_code": "...", // A string containing the raw, vulnerable code snippet.
    "fixed_code": "..."      // A string containing the corrected, secure version of the code.
  }
}