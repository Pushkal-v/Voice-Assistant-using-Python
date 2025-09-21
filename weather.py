import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather(city_name):
    api_key = os.getenv('WEATHER_API_KEY')
    if not api_key:
        print("❌ Error: API key not found. Please check your .env file")
        return None
    url= f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'

    try:
        response = requests.get(url, timeout=10) 
        
        if response.status_code == 200:
            data = response.json()
            return {
                'city': city_name,
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'success': True
            }
        else:
            print(f"❌ Error: City '{city_name}' not found (Status code: {response.status_code})")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None
    
def format_weather(data):
    if not data or not data.get('success'):
        return "❌ Unable to retrieve weather data."
    
    return (f"🌤️ Weather in {data['city']}:\n"
            f"Temperature: {data['temperature']}°C\n"
            f"Feels like: {data['feels_like']}°C\n"
            f"Humidity: {data['humidity']}%\n"
            f"Description: {data['description'].capitalize()}")
def test_weather():
    test_cities = input("Enter city names separated by commas or a single city name : ").split(',')
    for city in test_cities:
        weather_data = get_weather(city)

        if weather_data:
            print(format_weather(weather_data))
        else:
            print(f"❌ Could not retrieve weather for {city}")

if __name__ == "__main__":
    test_weather()