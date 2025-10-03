import os
import requests
import time

BASE_URL = "https://sanctionslistservice.ofac.treas.gov"
OUTPUT_DIR = "output"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36"
}

def fetch_entities(list_name, program_name):
    """
    Fetch entities for a specific list and program.
    Saves the XML response to output/{list}-{program}.xml
    """
    start_time = time.time()  # start timer
    print(f"Starting fetch for list='{list_name}' and program='{program_name}'...")
    print("Start time for seaching is :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(start_time)))
    url = f"{BASE_URL}/entities"
    params = {"list": list_name, "program": program_name}

    print(f"Fetching entities for list='{list_name}' and program='{program_name}'...")
    resp = requests.get(url, headers=HEADERS, params=params, timeout=60)
    resp.raise_for_status()

    if resp.text.strip():  # only save non-empty responses
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"{list_name}_{program_name}.xml".replace(" ", "_")
        file_path = os.path.join(OUTPUT_DIR, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(resp.text)
        print(f"Saved: {file_path}")
    else:
        print("No data returned for this combination.")
    end_time = time.time()  # end timer
    print("End time for seaching is :", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(end_time)))
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
if __name__ == "__main__":
    # Example: fetch SDN entities under IRAN program
    list_name = "SDN"  # choose the list
    program_name = "IRAN"  # choose one program from the list
    print("Create a folder named 'output' to store the XML files.")
    fetch_entities(list_name, program_name)
