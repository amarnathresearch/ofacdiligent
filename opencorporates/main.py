import requests

def search_opensanctions(name: str):
    """
    Search OpenSanctions by entity name using the /search endpoint.
    """
    url = "https://api.opensanctions.org/search"
    payload = {"q": name}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print("HTTP request failed:", e)
        return []

    data = response.json()

    # Check structure skeptically
    results = data.get("results", [])
    if not results:
        print(f"No results found for '{name}'. Verify spelling or dataset coverage.")
        return []

    entities = []
    for item in results:
        entities.append({
            "id": item.get("id"),
            "name": item.get("caption"),
            "datasets": item.get("datasets", []),
            "schema": item.get("schema"),
        })
    return entities


if __name__ == "__main__":
    name_to_search = "Tesla"
    results = search_opensanctions(name_to_search)
    if results:
        print(f"\nFound {len(results)} result(s) for '{name_to_search}':")
        for e in results:
            print(f"- {e['name']} ({e['schema']}) | Datasets: {e['datasets']}")
    else:
        print("No matches found.")
