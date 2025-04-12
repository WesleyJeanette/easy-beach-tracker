import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def setup_openmeteo_client():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)
    return openmeteo

def collect_marine_weather_data(lat, lon):
    openmeteo = setup_openmeteo_client()

    url = "https://marine-api.open-meteo.com/v1/marine"
    # TODO: pass in option for location, not hardcoded
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ["wave_height", "wave_direction", "wave_period", "ocean_current_velocity", "ocean_current_direction", "sea_surface_temperature", "sea_level_height_msl"],
        "timezone": "America/New_York",
        "length_unit": "imperial",
        "wind_speed_unit": "mph"
    }
    responses = openmeteo.weather_api(url, params=params)

    # Add a for loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_wave_height = hourly.Variables(0).ValuesAsNumpy()
    hourly_wave_direction = hourly.Variables(1).ValuesAsNumpy()
    hourly_wave_period = hourly.Variables(2).ValuesAsNumpy()
    hourly_ocean_current_velocity = hourly.Variables(3).ValuesAsNumpy()
    hourly_ocean_current_direction = hourly.Variables(4).ValuesAsNumpy()
    hourly_sea_surface_temperature = hourly.Variables(5).ValuesAsNumpy()
    hourly_sea_level_height_msl = hourly.Variables(6).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
	    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}

    hourly_data["wave_height"] = hourly_wave_height
    hourly_data["wave_direction"] = hourly_wave_direction
    hourly_data["wave_period"] = hourly_wave_period
    hourly_data["ocean_current_velocity"] = hourly_ocean_current_velocity
    hourly_data["ocean_current_direction"] = hourly_ocean_current_direction
    hourly_data["sea_surface_temperature"] = hourly_sea_surface_temperature
    hourly_data["sea_level_height_msl"] = hourly_sea_level_height_msl

    return pd.DataFrame(data = hourly_data)

def describe_marine_weather_data(df):
    return f'Marine Data Description: Wave Height {df["wave_height"].iloc[0]}, Wave Direction {df["wave_direction"].iloc[0]}, Wave Period {df["wave_period"].iloc[0]}, Ocean Current Velocity {df["ocean_current_velocity"].iloc[0]}, Ocean Current Direction {df["ocean_current_direction"].iloc[0]}'        

def collect_weather_forcast_data(lat, lon):
    openmeteo = setup_openmeteo_client()
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	    "latitude": lat,
	    "longitude": lon,
	    "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "wind_direction_10m"],
	    "timezone": "America/New_York",
	    "wind_speed_unit": "mph",
	    "temperature_unit": "fahrenheit"
        # "past_days": 1,
        # "forcast_days": 1
    }
    # TODO: pass in option for location, not hardcoded
    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    responses = openmeteo.weather_api(url, params=params)
    
    # Add a for loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(2).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(3).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
	    start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	    end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	    freq = pd.Timedelta(seconds = hourly.Interval()),
	    inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m
    hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
    hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
    hourly_data["wind_direction_10m"] = hourly_wind_direction_10m

    return pd.DataFrame(data = hourly_data)