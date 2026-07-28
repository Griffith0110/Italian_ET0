from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import streamlit as st


st.subheader("🌿 ET0", divider="green", text_alignment="center")

# Inserito un User-Agent identificativo per rispetare le policy di Nominatim
geolocator = Nominatim(user_agent="ET0")

# RateLimiter garantisce un intervallo minimo di 1 secondo tra le chiamate
geocode_with_rate_limit = RateLimiter(geolocator.geocode, min_delay_seconds=1)

# Cache per evitare che ad ogni re-run di Streamlit venga richiamato l'API per la stessa città


@st.cache_data(ttl=86400)
def get_location(query):
    return geocode_with_rate_limit(query, timeout=10)


location_query = st.text_input(
    "Geoposition",
)
if location_query:
    location = get_location(location_query)

    if location:
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)

        # Make sure all required weather variables are listed here
        # The order of variables in hourly or daily is important to assign them correctly below
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "daily": ["et0_fao_evapotranspiration", "precipitation_sum"],
            "past_days": 61,
            "forecast_days": 16,
        }
        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]

        # Process daily data. The order of variables needs to be the same as requested.
        daily = response.Daily()
        daily_et0_fao_evapotranspiration = daily.Variables(0).ValuesAsNumpy()
        daily_precipitation_sum = daily.Variables(1).ValuesAsNumpy()

        daily_data = {
            "date": pd.date_range(
                start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=daily.Interval()),
                inclusive="left",
            ).tz_convert(None)
        }

        daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration
        daily_data["precipitation_sum"] = daily_precipitation_sum
        daily_data["et0_total"] = (
            daily_et0_fao_evapotranspiration - daily_precipitation_sum
        )

        daily_dataframe = pd.DataFrame(data=daily_data)
        with st.container(horizontal_alignment="center", border=True):
            st.badge(f" {location.address}", color="green", icon="🏙️")
            st.badge(
                f" {location.latitude} °N, {location.longitude} °E",
                color="yellow",
                icon="🧭",
            )
            st.badge(f" {location.latitude} m asl", color="blue", icon="🗻")
            st.divider()
            st.dataframe(daily_dataframe, hide_index=True, width="content")
            st.divider()
            st.bar_chart(
                daily_dataframe,
                x="date",
                y=["et0_total"],
                x_label="Days",
                y_label="mm/m²",
                stack=True,
            )
            st.caption(
                "Weather data by [Open-Meteo](https://open-meteo.com/) (CC BY 4.0) "
                "• Geocoding by [OpenStreetMap](https://www.openstreetmap.org/copyright)"
            )
