import requests
from bs4 import BeautifulSoup
import re

# Step 1: Set company CIK
CIK = "0001652044"  # Alphabet Inc.
headers = {"User-Agent": "MyApp/1.0"}  # SEC requires a User-Agent

# Step 2: Fetch submissions JSON
submissions_url = f"https://data.sec.gov/submissions/CIK{CIK.zfill(10)}.json"
resp = requests.get(submissions_url, headers=headers)
data = resp.json()

# Step 3: Find the most recent 10-K filing
filings = data["filings"]["recent"]
tenk_indices = [i for i, f in enumerate(filings["form"]) if f.upper() == "10-K"]

if not tenk_indices:
    print("No 10-K found")
    exit()

latest_index = tenk_indices[0]  # first in the list is the most recent
accession_number = filings["accessionNumber"][latest_index].replace("-", "")
filing_url = f"https://www.sec.gov/Archives/edgar/data/{int(CIK)}/{accession_number}/{filings['primaryDocument'][latest_index]}"

# Step 4: Download filing HTML
resp = requests.get(filing_url, headers=headers)
soup = BeautifulSoup(resp.content, "html.parser")
text = soup.get_text(separator="\n")

# Step 5: Find Exhibit 21 section
# Basic heuristic: "Exhibit 21" followed by table/list of subsidiaries
exhibit_match = re.search(r"Exhibit\s*21(.*?)(?=(Exhibit\s*\d+|SIGNATURES|Item\s*1|$))", text, re.S | re.I)
if not exhibit_match:
    print("Exhibit 21 not found in filing")
    exit()

subsidiary_text = exhibit_match.group(1)

# Step 6: Extract subsidiary names (simple line-based approach)
subsidiaries = []
for line in subsidiary_text.splitlines():
    line = line.strip()
    # Skip empty lines
    if not line:
        continue
    # Very simple heuristic: lines containing company names
    if re.search(r"\bInc\.|LLC|Ltd\.|Corporation|Corp\b", line, re.I):
        subsidiaries.append(line)

# Step 7: Output
print(f"Found {len(subsidiaries)} subsidiaries:")
for s in subsidiaries:
    print("-", s)
