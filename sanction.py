import requests

BASE_URL = "https://sanctionslistservice.ofac.treas.gov"

def check_service_alive():
    """Check if the OFAC SLS service is reachable."""
    try:
        resp = requests.get(f"{BASE_URL}/alive", timeout=10)
        if resp.status_code == 200:
            print("✅ OFAC SLS service is reachable")
            return True
        else:
            print(f"⚠️ Service returned status code {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not reach OFAC SLS service: {e}")
        return False

def fetch_entities(list_name="SDN"):
    """Fetch entities from the specified list."""
    url = f"{BASE_URL}/entities?list={list_name}"
    headers = {"Accept": "application/json"}  # force JSON response
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()  # may raise JSONDecodeError if not JSON
        return data.get("entities", [])
    except requests.exceptions.JSONDecodeError:
        print("⚠️ Response was not valid JSON. Possibly HTML or empty response.")
        print("Response preview:", resp.text[:500])
        return []
    except Exception as e:
        print(f"❌ Error fetching entities: {e}")
        return []

def search_entities(entities, name, country=None):
    """Filter entities locally by name and optional country."""
    name = name.lower()
    country = country.lower() if country else None
    results = []
    for e in entities:
        entity_name = e.get("name", "").lower()
        addresses = e.get("addresses", [])
        countries = [a.get("country", "").lower() for a in addresses if a.get("country")]
        if name in entity_name:
            if country:
                if country in countries:
                    results.append(e)
            else:
                results.append(e)
    return results

def main():
    if not check_service_alive():
        print("Cannot proceed without reachable OFAC SLS service.")
        return

    list_name = "SDN"  # default list
    name_input = input("Enter entity name to check: ").strip()
    country_input = input("Enter country (optional): ").strip() or None

    entities = fetch_entities(list_name)
    if not entities:
        print("No entities fetched. Check the endpoint or network.")
        return

    matches = search_entities(entities, name_input, country_input)

    if matches:
        print(f"⚠️ Possible OFAC matches for '{name_input}' ({country_input}):")
        for m in matches:
            print(f"Name: {m.get('name')}, Addresses: {m.get('addresses')}")
    else:
        print(f"✅ No OFAC match found for '{name_input}' ({country_input})")

if __name__ == "__main__":
    main()
