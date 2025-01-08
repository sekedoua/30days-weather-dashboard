import os
import json
import boto3
import requests
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherDashboard:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')
        self.s3_client = boto3.client('s3')

    def create_bucket_if_not_exists(self):
        """Create S3 bucket if it doesn't exist"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} exists")
        except:
            print(f"Creating bucket {self.bucket_name}")
        try:
            # Simpler creation for us-east-1
            self.s3_client.create_bucket(Bucket=self.bucket_name)
            print(f"Successfully created bucket {self.bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")

    def fetch_weather(self, city):
        """Fetch weather data from OpenWeather API"""
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def fetch_forcast(self, city):
        """Fetch forcasy data from OpenWeather API"""
        base_url_forcast = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": self.api_key,
            "units": "metric"
        }
        
        try:
            response = requests.get(base_url_forcast, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching weather data: {e}")
            return None

    def save_to_s3(self, weather_data,forcast_data, city):
        """Save weather data to S3 bucket"""
        if not weather_data or not forcast_data :
            return False
            
        timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
        file_name_weather = f"weather-data/{city}-{timestamp}.json"
        file_name_foracast = f"forcast-data/{city}-{timestamp}.json"
        try:
            weather_data['timestamp'] = timestamp
            forcast_data['timestamp'] = timestamp
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name_weather,
                Body=json.dumps(weather_data),
                ContentType='application/json'
            )
            print(f"Successfully saved weather data for {city} to S3")
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_name_foracast,
                Body=json.dumps(forcast_data),
                ContentType='application/json'
            )
            print(f"Successfully saved forcast data for {city} to S3")
            
            return True
        
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return False
        

def main():
    dashboard = WeatherDashboard()
    
    # Create bucket if needed
    dashboard.create_bucket_if_not_exists()
    
    cities = ["Philadelphia", "Seattle", "New York","Paris","Abidjan","Cotonou","Dallas","Addis-Abeba"]
    
    for city in cities:
        print(f"\nFetching weather and 5 days forcast for {city}...")
        weather_data = dashboard.fetch_weather(city)
        forcast_data= dashboard.fetch_forcast(city)
        if weather_data or forcast_data :
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            min_temp_forcast= forcast_data['list'][0]['main']['temp_min']
            max_temp_forcast= forcast_data ['list'][0]['main']['temp_max']
            prec_prob = forcast_data['list'][0]['pop']
        
            print(f"Temperature: {temp}°C")
            print(f"Feels like: {feels_like}°C")
            print(f"Humidity: {humidity}%")
            print(f"Conditions: {description}")
            print(f"Max temperature forcast :{max_temp_forcast}°C")
            print(f"Min temperature forcast :{min_temp_forcast}°C")
            print(f"Probability of precipitation :{prec_prob*100}%")
      

            # Save to S3
            success = dashboard.save_to_s3(weather_data,forcast_data,city)
            if success:
                print(f"Weather and forcast data for {city} saved to S3!")
        else:
            print(f"Failed to fetch weather or forcast data for {city}")

if __name__ == "__main__":
    main()