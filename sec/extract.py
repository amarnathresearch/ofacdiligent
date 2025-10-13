import requests
import json

def extract_company_info_from_url(json_url):
    response = requests.get(json_url)
    data = response.json()

    # Entity Confirmation & Metadata
    entity = {
        "registered_legal_name": data.get('issuer', {}).get('name', ''),
        "country_of_incorporation": data.get('issuer', {}).get('stateOfIncorporation', ''),
        "incorporation_date": data.get('issuer', {}).get('incorporationDate', ''),
        "registered_business_address": ', '.join(filter(None, [
            data.get('issuer', {}).get('businessStreet', ''),
            data.get('issuer', {}).get('businessCity', ''),
            data.get('issuer', {}).get('businessState', ''),
            data.get('issuer', {}).get('businessZipCode', ''),
            data.get('issuer', {}).get('businessPhone', ''),
            data.get('issuer', {}).get('businessFax', '')
        ])),
        "cik": data.get('cik', ''),
        "lei": data.get('issuer', {}).get('lei', ''),
        "duns": data.get('issuer', {}).get('duns', ''),
        "ein": data.get('issuer', {}).get('ein', '')
    }

    # Principals - Directors, Executives
    principals = []
    officers = data.get('officers', [])
    for officer in officers:
        principals.append({
            "full_legal_name": officer.get('name', ''),
            "nationality": officer.get('nationality', ''),
            "date_of_birth": officer.get('birthDate', ''),
            "position/title": officer.get('title', ''),
            "ownership_percentage": officer.get('ownershipPct', ''),
            "address": officer.get('address', entity['registered_business_address'])
        })

    # Company Profile Enrichment
    profile = {
        "business_description": data.get('business', {}).get('description', ''),
        "industry": data.get('business', {}).get('industry', ''),
        "core_products_services": data.get('business', {}).get('productsServices', ''),
        "num_employees": data.get('business', {}).get('numEmployees', ''),
        "annual_revenue": data.get('financials', {}).get('annualRevenue', ''),
        "annual_sales": data.get('financials', {}).get('annualSales', ''),
        "website_url": data.get('business', {}).get('website', '')
    }

    return {
        "entity": entity,
        "principals": principals,
        "profile": profile
    }

# Usage
url = "https://data.sec.gov/submissions/CIK0000320193.json"
result = extract_company_info_from_url(url)
print(json.dumps(result, indent=2))
