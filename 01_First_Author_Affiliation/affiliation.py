#Import Libraries
import pandas as pd
import logging
from Bio import Entrez
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Current notebook's directory
base_dir = Path.cwd().parent  # Moves one level up from current working directory

# Paths
credentials_path = base_dir / '00_Local' / '01_Configs' / 'credentials.txt'
data_dir = base_dir / '00_Local' / '02_Data'
publications_file = data_dir / 'ZNPHI_Pubmed.csv'
output_file = data_dir / 'ZNPHI_Pubmed_Updated.csv'

# Step_1
logger.info("Packages installed and Path set")


# Read Credentials txt file for API_KEY
credentials = {}
with credentials_path.open('r') as file:
    for line in file:
        if '=' in line:
            key, value = line.strip().split('=', 1)
            credentials[key.strip()] = value.strip()

# Extract values
API_KEY = credentials.get('API_KEY')
EMAIL = credentials.get('EMAIL')

# Step_2
logger.info("API Key Collected")


# Configure Entrez
Entrez.email = EMAIL
Entrez.api_key = API_KEY

# Step_2
logger.info("API Key Collected")

# Step_3: Load Publications File
try:
    data = pd.read_csv(publications_file)
    logger.info(f"Loaded publications file with {len(data)} rows")
except Exception as e:
    logger.error(f"Error loading publications file: {e}")
    raise

# Step_4: Define function to fetch affiliation
def fetch_affiliation(doi):
    try:
        # Search PubMed for the DOI
        handle = Entrez.esearch(db="pubmed", term=doi, retmax=1)
        record = Entrez.read(handle)
        handle.close()
        
        # Get PubMed ID (PMID)
        if "IdList" in record and len(record["IdList"]) > 0:
            pmid = record["IdList"][0]
            # Fetch detailed metadata for the article
            handle = Entrez.efetch(db="pubmed", id=pmid, rettype="xml", retmode="text")
            records = Entrez.read(handle)
            handle.close()
            
            # Extract first author affiliation
            article = records["PubmedArticle"][0]
            authors = article["MedlineCitation"]["Article"]["AuthorList"]
            first_author = authors[0]
            return first_author.get("AffiliationInfo", [{}])[0].get("Affiliation", "Affiliation not found")
        else:
            return "DOI not found in PubMed"
    except Exception as e:
        logger.error(f"Error fetching affiliation for DOI {doi}: {e}")
        return "Error during API fetch"

# Step_5: Fetch affiliations for all rows
if "DOI" not in data.columns:
    logger.error("The input file does not contain a 'DOI' column")
    raise KeyError("Missing 'DOI' column in input file")

logger.info("Fetching affiliations for each DOI...")
affiliations = []

for index, row in data.iterrows():
    doi = row["DOI"]
    logger.info(f"Processing DOI: {doi}")
    affiliation = fetch_affiliation(doi)
    affiliations.append(affiliation)

logger.info("Affiliation fetching complete")

# Step_6: Update DataFrame and Save
data["Affiliation of First Author"] = affiliations

try:
    data.to_csv(output_file, index=False)
    logger.info(f"Updated data saved to {output_file}")
except Exception as e:
    logger.error(f"Error saving updated file: {e}")
    raise