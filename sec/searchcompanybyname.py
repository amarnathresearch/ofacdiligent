import json

def search_companies_by_name(json_file, name_prefix):
    """
    Search for companies whose names start with `name_prefix` (case-insensitive).
    Returns a list of matching dictionaries.
    """
    with open(json_file, "r", encoding="utf-8") as f:
        companies = json.load(f)

    prefix_lower = name_prefix.lower()
    results = [c for c in companies if c["CompanyName"].lower().startswith(prefix_lower)]
    return results


# Example usage:
json_file = "input/unique_companies.json"
search_term = "alphabet"
matches = search_companies_by_name(json_file, search_term)

for company in matches:
    print(f"{company['CIK']} | {company['CompanyName']}")
if company:
    print(company['CIK'])

print(f"✅ Found {len(matches)} companies starting with '{search_term}'")
