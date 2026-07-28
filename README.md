# Italian_ET0

A small Streamlit app to retrieve and visualize daily reference evapotranspiration (ET0) for locations in Italy using the Open-Meteo API.

Features
- Search by city, address, region, or enter "Italy" for a national overview.
- Uses Open-Meteo daily variables: `et0_fao_evapotranspiration` and `precipitation_sum`.
- Displays a table of daily values and an interactive bar chart for a combined `et0_total`.

Installation
1. Create and activate a virtual environment:
   - python -m venv .venv
   - On macOS/Linux: `source .venv/bin/activate`
   - On Windows: `.venv\Scripts\activate`
2. Install dependencies:
   - `pip install -r requirements.txt`

Run
- From the repository root: `streamlit run main.py`

Notes
- Geocoding is done with Nominatim (OpenStreetMap); please respect its usage policy and rate limits.
- Responses are cached locally to reduce API calls.

License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Contributing
Contributions welcome. Open an issue or submit a PR.
