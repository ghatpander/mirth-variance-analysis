# Mirth Integration Analyzer - Variation between different channel transformers

## Overview
This tool is a custom-built integration audit engine I developed to streamline the review and comparison of Mirth Connect (NextGen Connect) transformer steps across different client EMR environments. 

Instead of manually digging through XML channel files, this dashboard parses the channel configuration, extracts the JavaScript transformer code, and provides an automated, logical comparison against a baseline schema.

## Key Capabilities
- **Automated XML Parsing**: Directly ingests exported Mirth channel XML files and identifies all `JavaScriptStep` components.
- **Side-by-Side Comparison**: Displays transformer code from multiple clients in a clean, scrollable interface, making it easy to spot logic differences at a glance.
- **Automated Variance Analysis**: Uses AI to perform a technical audit of each transformer step. It assesses code logic, checks for adherence to standard HL7-to-JSON mapping patterns, and assesses structural complexity.
- **Layout Optimization**: Features a custom-built, scrollable UI that keeps code blocks constrained and prevents the dashboard from stretching vertically.

## Prerequisites
- **Python 3.x** installed.
- **Streamlit**: `pip install streamlit`
- **BeautifulSoup4**: `pip install beautifulsoup4`
- **Internet Access**: Required for the AI-driven variance analysis (via Puter.js integration).

## Setup & Execution
1.  **Place the script**: Save `mirth_audit_dashboard.py` in your local project directory.
2.  **Launch the Dashboard**:
    Open your terminal in the script directory and run:
    ```bash
    python -m streamlit run mirth_audit_dashboard.py
    ```
3.  **Access**: The terminal will provide a local URL (usually `http://localhost:8501`). Open this in your web browser.
4.  **Audit**: Upload your client channel XML files via the file uploader, expand any transformer step, and click "Run" to trigger the audit.

## How it Works
The engine uses `BeautifulSoup` to extract the `script` nodes from the Mirth XML structure. When a variance analysis is triggered, it dynamically packages the code snippets from all uploaded files along with the project's baseline JSON schema and passes them to an LLM for a structured comparison. This allows for instant, context-aware feedback on mapping logic and clinical risk without hardcoded keyword rules.

## Maintenance
- **Updating the Baseline**: The `BASELINE_JSON` variable at the top of the script defines the target structure. Modify this schema as your integration standards evolve.
- **Scaling**: To compare more than two clients, simply upload additional XML files; the dashboard dynamically generates comparison columns for every uploaded file.
