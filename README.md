# Italian_ET0

A small Streamlit app to retrieve and visualize daily reference evapotranspiration (ET0) for Italian locations using the Open-Meteo API.

ET0 in this project is calculated using the FAO evapotranspiration values provided by Open-Meteo and is combined with precipitation to show a daily "ET0 total" (et0_fao_evapotranspiration − precipitation_sum).

## Features
- Search by city, address, region, or enter `Italy` for a national overview.
- Uses Open-Meteo daily variables:
  - et0_fao_evapotranspiration
  - precipitation_sum
- Displays a table of daily values and an interactive bar chart.
- Implements response caching and retry logic for resilient API access.

## How it works (based on `main.py`)
1. The app uses `geopy` (Nominatim) to geocode the user's input location.
2. It constructs a request to the Open-Meteo API asking for daily data:
   - 61 past days (`past_days: 61`)
   - 16 forecast days (`forecast_days: 16`)
   - daily variables: `et0_fao_evapotranspiration`, `precipitation_sum`
3. The response is parsed into a pandas DataFrame with:
   - `date`
   - `et0_fao_evapotranspiration`
   - `precipitation_sum`
   - `et0_total` = `et0_fao_evapotranspiration - precipitation_sum`
4. The UI (Streamlit) shows badges with location metadata, a dataframe, and a bar chart for `et0_total`.
5. The app uses a cached requests session (`requests_cache`) with a retry wrapper (`retry_requests`) to improve reliability and reduce API calls.

## Installation

Recommended: create a virtual environment.

- Using pip:
  1. Create and activate a virtual environment:
     - python -m venv .venv
     - On macOS/Linux: source .venv/bin/activate
     - On Windows: .venv\Scripts\activate
  2. Install dependencies:
     - pip install -r requirements.txt

## Run

From the repository root:
- streamlit run main.py

Open the displayed local URL in your browser, enter a location (e.g., "Rome, Italy" or just "Italy") and the app will show the ET0 data and charts.

## Configuration & Notes
- The app uses Nominatim (OpenStreetMap) for geocoding. Respect Nominatim's usage policy and rate limits: use a descriptive `user_agent` and avoid heavy automated querying.
- Responses are cached in a local folder named `.cache` with a 1-hour expiry to reduce repeated API calls.
- Retries are configured with up to 5 attempts and a small backoff to handle transient network errors.
- Time range: the app requests 61 past days and 16 forecast days. Modify `past_days` and `forecast_days` in `main.py` if you need a different window.
- Units: ET0 and precipitation are shown in mm (mm/m² for ET0_total display label).

## Dependencies (core)
- Python 3.8+
- streamlit
- geopy
- openmeteo-requests
- pandas
- requests-cache
- retry-requests

## Limitations & TODO
- No explicit error handling for missing geocoding results (e.g., when the location is not found). We can add user-friendly messages.
- No tests included.
- Consider adding:
  - A configuration panel to select date ranges or variables.
  - Export (CSV) functionality for the resulting DataFrame.
  - Unit tests and CI.

## Contributing
Contributions are welcome. Open an issue or PR describing your change. If you want, I can prepare a PR that:
- Adds `README.md` to the repo (this file),
- Creates `requirements.txt`,
- Adds a basic `.gitignore` and optional LICENSE (MIT by default).

## License
Add a license file (e.g., `LICENSE` with MIT) if you want this project to be openly licensed. I can add one for you — tell me which license you'd prefer.

---
