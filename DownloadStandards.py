import os
import json
import requests
import pandas as pd
import time
import traceback

API_KEY = "YOUR_API_KEY"
BASE_URL = "http://commonstandardsproject.com/api/v1"
HEADERS = {"Api-Key": "bAmFakqP1SfKcSt8ef4XawZB"}

def get_state_standard_set_ids(state):
    resp = requests.get(f"{BASE_URL}/jurisdictions/", headers=HEADERS)
    resp.raise_for_status()
    jurisdictions = resp.json()["data"]
    state_id = next(j["id"] for j in jurisdictions if j["title"].lower() == state)

    resp = requests.get(f"{BASE_URL}/jurisdictions/{state_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()["data"]["standardSets"]

def find_ngss_jurisdiction():
    resp = requests.get(f"{BASE_URL}/jurisdictions/", headers=HEADERS)
    resp.raise_for_status()
    jurisdictions = resp.json()["data"]
    for j in jurisdictions:
        if "next generation" in j["title"].lower() or "ngss" in j["title"].lower():
            print(f"NGSS Found: {j['title']}, ID: {j['id']}")
            return j
    raise ValueError("NGSS jurisdiction not found")

def download_and_save_standards(standard_sets, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    df = pd.DataFrame()
    for sset in standard_sets:
        set_id = sset["id"]

        resp = requests.get(f"{BASE_URL}/standard_sets/{set_id}", headers=HEADERS)
        resp.raise_for_status()
        standards = resp.json()["data"]["standards"]

        # resp.json()["data"]
        data = resp.json()["data"]
        setTitle = data["title"]
        subject = data["subject"]
        gradeLevels = data["educationLevels"]
        sourceURL = sset["document"]["sourceURL"]
        valid = data['document'].get("valid", None)

        for std_id, std in standards.items():
            filename = f"{output_dir}/{std_id}.json"

            std["title"] = setTitle
            std["subject"] = subject
            std["gradeLevels"] = gradeLevels
            std["sourceURL"] = sourceURL
            std["valid"] = valid
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(std, f, ensure_ascii=False, indent=2)
            df = pd.concat([df, pd.DataFrame([std])], ignore_index=True)

        print(f"Downloaded {len(standards)} standards from set: {sset['title']}")
    # df.to_csv('Outputs/standards_check.csv', index=False)

def convert_json_to_csv(json_folder, csv_filename):
    all_data = []
    for file in os.listdir(json_folder):
        if file.endswith(".json"):
            with open(os.path.join(json_folder, file), "r", encoding="utf-8") as f:
                std = json.load(f)
                all_data.append(std)
    df = pd.DataFrame(all_data)
    df.to_csv(csv_filename, index=False)
    print(f"Saved {len(df)} standards to {csv_filename}")

# Run the process
if __name__ == "__main__":
    us_states = [
        "next generation science standards", "alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut",
        "delaware", "florida", "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa",
        "kansas", "kentucky", "louisiana", "maine", "maryland", "massachusetts", "michigan",
        "minnesota", "mississippi", "missouri", "montana", "nebraska", "nevada", "new hampshire",
        "new jersey", "new mexico", "new york", "north carolina", "north dakota", "ohio",
        "oklahoma", "oregon", "pennsylvania", "rhode island", "south carolina", "south dakota",
        "tennessee", "texas", "utah", "vermont", "virginia", "washington", "west virginia",
        "wisconsin", "wyoming", "district of columbia"
    ]
    # us_states = ["next generation science standards"]

    # ngss = find_ngss_jurisdiction()

    for state in us_states:
        try:
            print(f"Processing: {state.title()}")
            sets = get_state_standard_set_ids(state)
            output_dir = f"Outputs/standards_json_{state}"
            csv_file = f"Outputs/{state}_standards.csv"

            os.makedirs(output_dir, exist_ok=True)

            download_and_save_standards(sets, output_dir)
            convert_json_to_csv(output_dir, csv_file)

        except Exception as e:
            print(f"Failed to process {state}: {e}")
            traceback.print_exc()
    time.sleep(1)

breakpoint()

