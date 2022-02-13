import requests
import json

# This script is to reach out to NWS for the Midlothian area and return forecast data
api_url = "https://api.weather.gov/gridpoints/AKQ/40,73/forecast"


def weather():
    # Call to NWS for weather data local to Chesterfield
    time_period = []
    temperature = []
    forecast = []
    try:
        response = requests.get(url=api_url)
        json_response = json.loads(response.content)

        for period in json_response["properties"]["periods"]:
            if period["number"] <= 3:
                current_period = period["name"]
                temp = period["temperature"]
                detailed_forecast = period["detailedForecast"]
                time_period.append(current_period)
                temperature.append(temp)
                forecast.append(detailed_forecast)

    except requests.exceptions.RequestException as err:
        print("HTTP Request failed")
        print(err)

    return time_period, temperature, forecast


if __name__ == "__main__":
    weather()
