
# 📚 Common Standards Project (CSP) Data Extractor

This project provides a Python script for downloading and organizing U.S. K–12 educational standards using the [Common Standards Project API](http://commonstandardsproject.com/api/v1). The goal is to centralize and preserve curriculum standards from all 50 U.S. states, including support for NGSS, Science, ELA, and other subjects.

---

## 🚀 Features

- ✅ Extracts curriculum standards from the CSP API
- ✅ Supports batch processing across all U.S. states
- ✅ Saves each standard as an individual JSON file
- ✅ Converts standards into a CSV file for review or analysis
- ✅ Captures metadata like subject, grade levels, source URL, and validity

---

## 🔧 Requirements

- Python 3.7+
- Modules:
  - `requests`
  - `pandas`

Install dependencies with:

```bash
pip install -r requirements.txt
````

---

## 🔐 Authentication

You must request and include a valid API key from [commonstandardsproject.com](http://commonstandardsproject.com/api/v1).

Set your API key in the script under:

```python
HEADERS = {"Api-Key": "YOUR_API_KEY"}
```

---

## 🧮 Usage

### Run the Script

```bash
python main.py
```

By default, the script downloads standards for a predefined list of states (can be adjusted in the `us_states` list).

### Output

* Standards saved as:
  `Outputs/standards_json_<state>/<standard_id>.json`

* CSV summary for each state:
  `Outputs/<state>_standards.csv`

---

## 📁 File Structure

```bash
.
├── main.py
├── Outputs/
│   ├── standards_json_<state>/
│   └── <state>_standards.csv
├── requirements.txt
└── README.md
```

---

## 📄 Sample Output (JSON)

```json
{
  "id": "0A0AF1D1EFCC49348BCDEAFD7A3D91FD",
  "asnIdentifier": "S2661324",
  "description": "Productive (creation of oral presentations and written texts)",
  "SetTitle": "Grades 9, 10",
  "Subject": "English Language Development (2012-)",
  "GradeLevels": ["09", "10"],
  "sourceURL": "http://www.cde.ca.gov/sp/el/er/documents/eldstndspublication14.pdf",
  "valid": null
}
```

---

## 📌 Notes

* If re-running, the script checks for existing output folders.
* To avoid duplicate downloads, you can uncomment the conditional skip logic for CSV existence.

