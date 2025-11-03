import json

# Load the JSON (replace 'data.json' with your filename if needed)
with open("apple.json", "r") as f:
    data = json.load(f)

# Defensive check: ensure data is a list with expected structure
if not isinstance(data, list) or not data:
    raise ValueError("Unexpected JSON format — top-level list missing or empty.")

company_info = data[0]

# Extract company name
company_name = company_info.get("sec_data", {}).get("company_name")

# Extract executive names, removing duplicates
executives = company_info.get("executives", [])
executive_names = sorted(set(exec.get("name") for exec in executives if "name" in exec))

# Print results
print("Company Name:", company_name)
print("Executives:")
for name in executive_names:
    print("-", name)


# 71ae6b9278c6c9aa141805d89191cab9b1ceb4fa

import requests
import json

# Replace this with your actual Serper API key
API_KEY = "71ae6b9278c6c9aa141805d89191cab9b1ceb4fa"

def search_executive(executive_name, company_name):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Query: executive name + company for better precision
    # payload = {
    #     "q": f"{executive_name} {company_name} sanctions"
    #     # "q": f"Tim Cook Apple Inc"
    # }
    # payload = {
    #     "q": f'("{company_name}" OR "{executive_name}") ("OFAC list" OR "EU sanctions list" OR "UN sanctions list" OR "UK sanctions list" OR "SDN list" OR "sanctioned entity") site:gov OR site:europa.eu OR site:un.org -news'
    # }
    # payload = {
    #     "q": f'("{executive_name}") ("OFAC list" OR "EU sanctions list" OR "UN sanctions list" OR "UK sanctions list" OR "SDN list" OR "sanctioned entity") site:gov OR site:europa.eu OR site:un.org -news'
    # }
    # payload = {
    #     "q": f'("{company_name}") ("OFAC list" OR "EU sanctions list" OR "UN sanctions list" OR "UK sanctions list" OR "SDN list" OR "sanctioned entity") site:gov OR site:europa.eu OR site:un.org -news'
    # }
    payload = {
        "q": f'("{executive_name} {company_name}") ("OFAC list" OR "EU sanctions list" OR "UN sanctions list" OR "UK sanctions list" OR "SDN list" OR "sanctioned entity") site:gov OR site:europa.eu OR site:un.org -news'
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()

    # Extract relevant fields cautiously
    results = []
    for result in data.get("organic", []):
        entry = {
            "title": result.get("title"),
            "link": result.get("link"),
            "snippet": result.get("snippet")
        }
        results.append(entry)

    # Save to JSON file
    output_filename = f"output/{company_name.lower().replace(' ', '_')}_{executive_name.lower().replace(' ', '_')}_search_results.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(results)} results to {output_filename}")

for name in executive_names:
    # print("-", name)
    search_executive(name, company_name)
search_executive("", company_name)
    # Example: search for Tim Cook
# search_executive(executivename, company_name)
