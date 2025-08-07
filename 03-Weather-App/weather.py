import tkinter as tk
import requests #python library to send HTTP requests like GET and POST

API_KEY = "184f7502ae538fb4468ec885d584741c"  # replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather" #root link for the weather API endpoint

def get_weather(city): #we create a function which takes the city name as input
    city = city_entry.get().strip()
    if not city:
        result_label.config(text="Please enter a city name.")
        return
    try:
        params = { #a dictionary containing the query parameters
            "q" : city,
            "appid" : API_KEY,
            "units" : "metric"
        }
        response = requests.get(BASE_URL, params=params, timeout=5) #sends a GET request to the API with these paramters.
        #timeout if API doesn't respond within 5 seconds, it stops trying.

        #Handling HTTP response codes

        if response.status_code == 401: #wrong API key.
            return "❌ Invalid API Key. Please check you key" #for emoji windows + . 
        elif response.status_code == 404: #City not found
            return f"❌City '{city}' not found. Please check the spelling."
        elif response.status_code != 200: #Other codes regarding API issue or server down
            return f"⚠️ API returned an error : {response.status_code}"
        
        #parsing JSON data
        data = response.json() #.json concerts APIs JSON respinse into a python dictionary
        #extracting useful info
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        #Formatting output
        return (
            f"\n 📍Weather in {city.capitalize()}:\n" #capitalize makes first letter of the city name uppaercase
            f" 🌡️Temperature : {temp}°C\n"
            f" ☁️ Condition : {weather}\n"
            f" 💧 Humidity : {humidity}%\n"
            f" 💨 Wind Speed : {wind_speed}m/s"
        )
    
    #Handling Connection Errors
    except requests.exceptions.ConnectionError:
        return "🛜 No internet Connection. Please check you network."
    except requests.exceptions.Timeout:
        return "⌛The request timed out. Try again later."
    except Exception as e:
        return f"⚠️ An unexcepted error occurred : {str(e)}"
    
def show_weather():
    city = city_entry.get() #reads whatever text the user typed in input box
    if city.strip() == "":
        result_label.config(text = "Please enter a city name.") 
    else:
        weather_info = get_weather(city)
        result_label.config(text=weather_info)

#Tkinter UI
root = tk.Tk() #creates the main application window
root.title("Weather App") #sets window title
root.geometry("400x300") #window size in pixels
root.config(bg="#e0f7fa") #background color for the window

#creates a label for the title of the app
title_label = tk.Label(root, text="Weather App", font=("Helvetica",16,"bold"), bg="#e0f7fa")
title_label.pack(pady=10) #places it at the top with 10px vertical padding

#tells the user to enter a city name
instruction_label = tk.Label(root, text="Please enter a city name", font=("Helvetica",12), bg="#e0f7fa", fg="green")
instruction_label.pack(pady=5)

#Entry widget : text input where the user types city name
city_entry = tk.Entry(root, font=("Helvetica",14))
city_entry.pack(pady=5)

#button get weather when clicked runs show_weather() fucntio 
get_weather_btn = tk.Button(root, text="Get Weather",font=("Helvetica", 12), command = show_weather)
get_weather_btn.pack(pady=5)

#result label where weather results or error mssgs will appear
result_label = tk.Label(root, text="", font=("Helvetica", 12),justify="left", bg="#e0f7fa", fg="black")
result_label.pack(pady=10)

#keeps the window running and interactive until closed by the user.
root.mainloop()
    
