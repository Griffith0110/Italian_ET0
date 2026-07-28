from geopy import location
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderTimedOut
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import streamlit as st

st.subheader("🌿 ET0", divider="green", text_alignment="center")

# Usiamo la cache di Streamlit per evitare di fare troppe richieste a Nominatim
@st.cache_data(ttl=3600)
def get_location(query):
    # Passa un user_agent unico e un timeout adeguato
    geolocator = Nominatim(user_agent="italian_et0_streamlit_app_v1", timeout=10)
    try:
        return geolocator.geocode(query)
    except (GeocoderUnavailable, GeocoderTimedOut):
        return None

location_query = st.text_input("Geolocation").strip()

if location_query:
    location = get_location(location_query)
    
    if location is None:
        st.error("Servizio di geolocalizzazione momentaneamente non disponibile o luogo non trovato. Riprova tra poco.")
    else:
        cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        openmeteo = openmeteo_requests.Client(session=retry_session)
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
        daily_data["et0_total"] = daily_et0_fao_evapotranspiration - daily_precipitation_sum
        daily_dataframe = pd.DataFrame(data=daily_data)
        
        with st.container(horizontal_alignment="center", border=True):
            st.badge(f" {location.address}", color="green", icon="🏙️")
            st.badge(
                f" {location.latitude:.4f} °N, {location.longitude:.4f} °E",
                color="yellow",
                icon="🧭",
            )
            # Nota: location.latitude non è l'altitudine. Se vuoi l'altitudine servirebbe la quota da Open-Meteo.
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
