import os
import json
import requests


def extract_unique_json(input_file, output_file):
    """
    Reads a master.idx-like file, extracts unique CIK and CompanyName,
    and saves them to a JSON file.
    """
    unique_companies = {}

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # skip headers, separators, empty lines, or comment lines
            if not line or line.startswith("CIK") or line.startswith("---") or line.startswith("Description:"):
                continue
            parts = line.split("|")
            if len(parts) >= 2:
                cik = parts[0].strip()
                name = parts[1].strip()
                unique_companies[cik] = name

    # convert to list of dicts
    output_data = [{"CIK": cik, "CompanyName": name} for cik, name in sorted(unique_companies.items())]

    # save JSON
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"✅ Extracted {len(output_data)} unique companies into {output_file}")


# Example usage:

# Step 1: save the master.idx file inside input folder
url = "https://www.sec.gov/Archives/edgar/full-index/2025/QTR3/master.idx"


# Step 2: extract JSON from saved file
extract_unique_json("input/master.idx", "input/unique_companies.json")
