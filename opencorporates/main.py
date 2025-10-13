import requests

company = "Apple Inc"
country = "United States"

# OpenCorporates (free tier)
r = requests.get(f"https://api.opencorporates.com/v0.4/companies/search?q={company}&country_code=us")
data = r.json()
# parse data["results"]["companies"][0]["company"]...
print(data)