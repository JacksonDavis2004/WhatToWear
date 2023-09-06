import openai
import smtplib
import requests

openai.api_key = "YOUR_API_KEY_HERE" # retrived from openai.com

# input the message sender and receiver
sender = "YOUR_EMAIL_HERE" 
password = "YOUR_EMAIL_PASSWORD_HERE"
subject = "WhatToWear Today" 

def chat(prompt):
    completions = openai.Completion.create(
        engine= "text-davinci-002",
        prompt=prompt,
        max_tokens= 3000,
        n = 1,
        temperature=0.6, 
    )

    message = completions.choices[0].text
    return message

user_name = input("Hi there, what is your name? ")
receiver = input("What email address would you like to send this to? ")
user_city = input("What city are you in? ")

weather_api_key = "YOUR_API_KEY_HERE" # retrived from openweathermap.org
weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={user_city}&units=metric&appid={weather_api_key}"

response = requests.get(weather_url)
weather_data = response.json()

# Extracting relevant weather information
temperature = weather_data["main"]["temp"]
feels_like = weather_data["main"]["feels_like"]
pressure = weather_data["main"]["pressure"]
humidity = weather_data["main"]["humidity"]
temp_min = weather_data["main"]["temp_min"]
temp_max = weather_data["main"]["temp_max"]
wind_speed = weather_data["wind"]["speed"]
wind_deg = weather_data["wind"]["deg"]
cloudiness = weather_data["clouds"]["all"]
rain_1h = weather_data.get("rain", {}).get("1h", 0)
rain_3h = weather_data.get("rain", {}).get("3h", 0)
snow_1h = weather_data.get("snow", {}).get("1h", 0)
snow_3h = weather_data.get("snow", {}).get("3h", 0)

weather_data = f"""Temperature: {temperature}°C
Feels Like: {feels_like}°C
Pressure: {pressure} hPa
Humidity: {humidity}%
Min Temperature: {temp_min}°C
Max Temperature: {temp_max}°C
Wind Speed: {wind_speed} km/h
Wind Direction: {wind_deg}°
Cloudiness: {cloudiness}%
Rain (1h): {rain_1h} mm
Rain (3h): {rain_3h} mm
Snow (1h): {snow_1h} mm
Snow (3h): {snow_3h} mm
"""

AI_weather_description = chat("Here is the weather data you are to summarize:" + weather_data + ". Give me a 2 sentence summary of the weather data of " + user_city + ". Always refer to the data: Temperature, Feels Like, Max & Min Temperature, and Cloudiness." +
                              " Only mention the sections: Rain (1h) and Snow (1h) if they are not 0. Never mention Pressure, Wind Speed, Wind Direction, Rain (3h), Snow (3h).")

response = chat("Give me a positive and short personalized message that is a minimum of 20 words telling me what type of clothing I should wear if I want to feel comfortable outside today and I live in " 
                + user_city + "where the weather data is: " + weather_data + ". Do not mention any weather data, only what is recommended to be worn in a 20 word response.")


emailmessage = f"""From: {sender}
To: {receiver}
Subject: {subject}

Hi {user_name}, here is your Weather Recommendation for your day in {user_city}! 
{AI_weather_description} {response}
"""

emailmessage_bytes = emailmessage.encode('utf-8')

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

try:
    server.login(sender, password)
    print("Successfully logged in...")
    server.sendmail(sender, receiver, emailmessage_bytes)
    print("Message sent!")

except smtplib.SMTPAuthenticationError:
    print("Unable to sign in")
