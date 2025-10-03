import os
import requests
import time
BASE_URL = "https://sanctionslistservice.ofac.treas.gov"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def save_entity_xml(entity_id, output_dir="output"):
    """Fetch entity XML and save to output/{entity_id}.xml"""
    start_time = time.time()  # start timer
    print(f"Starting fetch for entity_id='{entity_id}'...")
    print("Start time for seaching is :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))

    url = f"{BASE_URL}/entities/{entity_id}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()

    os.makedirs(output_dir, exist_ok=True)  # ensure output/ exists
    file_path = os.path.join(output_dir, f"{entity_id}.xml")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(resp.text)

    print(f"Saved: {file_path}")
    end_time = time.time()  # end timer
    print("End time for seaching is :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
    return file_path


if __name__ == "__main__":
    entity_id = 30629  # example
    save_entity_xml(entity_id)
