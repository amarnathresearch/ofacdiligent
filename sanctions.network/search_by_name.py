import requests
import time
import json

import re
import json

def filter_sanctions(result, pattern):
    """
    Filter search_sanctions_rpc results by a regex pattern applied to the names array.
    Returns only records where at least one name matches.
    """
    regex = re.compile(pattern, re.IGNORECASE)
    filtered = []

    for record in result.get("data", []):
        matching_names = [name for name in record.get("names", []) if regex.search(name)]
        if matching_names:
            new_record = record.copy()
            new_record["names"] = matching_names  # keep only the matching names
            filtered.append(new_record)

    return filtered

def search_sanctions_rpc(name: str):
    url = "https://api.sanctions.network/rpc/search_sanctions"
    params = {"name": name}
    headers = {
        "Accept": "application/json"
    }

    start = time.perf_counter()
    response = requests.get(url, params=params, headers=headers, timeout=10)
    end = time.perf_counter()

    # Try to parse JSON (or fallback)
    try:
        data = response.json()
    except Exception as e:
        data = {"error": f"JSON parse error: {e}", "raw_text": response.text}

    return {
        "start_time": start,
        "end_time": end,
        "inference_time": end - start,
        "status_code": response.status_code,
        "data": data
    }

if __name__ == "__main__":
    # name_to_search = "Abou Ali"
    # name_to_search = "Johnathan Doughnut"
    # name_to_search = "Agridime"
    name_to_search = "GLOBAL VISION"
    result = search_sanctions_rpc(name_to_search)

    print(json.dumps(result, indent=2))
    # Convert spaces to \s* so it matches any amount of whitespace
    pattern = re.sub(r"\s+", r"\\s*", name_to_search)

    # Add start and end anchors if you want an exact match ignoring spacing
    pattern = f"{pattern}"
    print(pattern)
    filtered_results = filter_sanctions(result, pattern)

    print(json.dumps(filtered_results, indent=2))
