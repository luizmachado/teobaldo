import os
import requests
from langchain_core.tools import tool

# Chave OpenWeather
weather_api_key = os.environ.get("OPENWEATHER_API_KEY")

@tool
def get_weather_forecast(latitude, longitude):
    """
    Obtém a previsão do tempo atual para uma dada latitude e longitude.
    Retorna uma descrição concisa do tempo e a temperatura em graus Celsius.
    """
    url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?lat={latitude}&lon={longitude}"
            f"&appid={weather_api_key}"
            f"&units=metric&lang=pt_br"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        description = data['weather'][0]['description']
        temp = data['main']['temp']

        return f"A previsão do tempo para o local é: {temp}°C, {description}."
    except requests.exceptions.RequestException as e:
        return f"Erro ao obter a previsão do tempo: {str(e)}"


if __name__ == "__main__":
    lat = -23.5613
    lon = -46.6565
    print(f"\nBuscando condições do metereológicas em lat '{lat}' e lon '{lon}'...")
    print(get_weather_forecast.invoke({"latitude": lat, "longitude": lon}))


