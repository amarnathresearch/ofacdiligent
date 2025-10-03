import requests
import json
import os
import time

BASE_URL = "https://sanctionslistservice.ofac.treas.gov"
OUTPUT_DIR = "output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def fetch_sanctions_lists():
    start_time = time.time()
    print("Starting fetch for sanctions lists...")
    print("Start time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))

    url = f"{BASE_URL}/sanctions-lists"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    lists = resp.json()  # returns a list of strings (or objects)
    
    end_time = time.time()
    print("End time:", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

    return lists

def save_sanctions_lists(lists):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, "sanctions_lists.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(lists, f, indent=4)
    print(f"Saved sanctions lists to {file_path}")

if __name__ == "__main__":
    print("Create a folder named 'output' to store the JSON file.")
    lists = fetch_sanctions_lists()
    # Print list names
    print("\nSanctions Lists:")
    for l in lists:
        print(l)
    # Save JSON file
    save_sanctions_lists(lists)

