import requests

# Base URL for entities
url = "https://sanctionslistservice.ofac.treas.gov/entities"

try:
    response = requests.get(url)
    response.raise_for_status()  # Raise an error if the request failed
    entities = response.json()   # Convert response to Python data
    print("entities", entities)
    # Filter entities containing "Tesla" (case-insensitive)
    tesla_entities = [
        entity for entity in entities
        if "tesla" in entity.get("name", "").lower()
    ]

    if tesla_entities:
        for e in tesla_entities:
            print(f"Name: {e.get('name')}, ID: {e.get('id')}")
    else:
        print("No entities found with the name 'Tesla'.")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
