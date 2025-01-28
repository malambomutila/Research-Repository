# Project 01: First Author Affiliation Extractor

## Overview
This Python script automates the process of retrieving first author affiliations for academic publications using the NCBI E-utilities API. It processes a CSV file containing DOIs (Digital Object Identifiers) and fetches the corresponding first author affiliations from PubMed.

## Project Structure
```
research-repository/
├── 00_Local/
│   ├── 01_Configs/
│   │   └── credentials.txt
│   └── 02_Data/
│       ├── Publications.csv
│       └── Publications_Updated.csv
├── 01_First_Author_Affiliation/
│   └── affiliation.py
├── virtualenv/
├── .gitignore
├── LICENSE
└── README.md
```

## Prerequisites
- Python 3.x
- Required Python packages:
  - pandas
  - biopython
- NCBI E-utilities API credentials

## Setup
1. Clone this repository:
```bash
git clone https://github.com/yourusername/research-repository.git
cd research-repository
```

2. Create a credentials.txt file in `00_Local/01_Configs/` with your NCBI API credentials:
```
API_KEY=your_api_key_here
EMAIL=your_email@example.com
```

3. Install required packages:
```bash
pip install pandas biopython
```

## Input Data Format
The script expects a CSV file (`Publications.csv`) with at least one column:
- `DOI`: Digital Object Identifier for each publication

## Usage
1. Place your input CSV file in the `00_Local/02_Data/` directory
2. Run the script:
```bash
python affiliation.py
```

## Output
The script generates an updated CSV file (`Publications_Updated.csv`) with an additional column:
- `Affiliation of First Author`: Contains the retrieved affiliation information for each publication's first author

## Features
- Automated retrieval of first author affiliations from PubMed
- Error handling and logging
- Progress tracking for each DOI processed
- Configurable input/output paths
- Secure credential management

## Error Handling
The script includes comprehensive error handling for:
- Missing credentials
- Invalid API responses
- File I/O operations
- Missing or malformed DOIs
- Network connection issues

## Privacy and Security
- Credential files are excluded from version control
- API keys and email addresses are loaded securely from a local configuration file
- The `credentials.txt` file is listed in `.gitignore`

## Changes
Edit the lines below to match your CSV file and desired output file:
```bash
publications_file = data_dir / 'Publications.csv'
output_file = data_dir / 'Publications_Updated.csv'
```

## License
MIT License

## Acknowledgments
- NCBI E-utilities for providing the PubMed API
- Biopython developers for the excellent API wrapper
