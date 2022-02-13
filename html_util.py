import requests
import webbrowser
  
# Accessing the weather api and getting the real-time weather condition
def weather(city):
	API_ID = "[REDACTED]"
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_ID}"
	response = requests.get(url)

	if response.status_code == 200:
		data = response.json()
		weather = data['weather'][0]['description']
		return weather

	else: return "ERROR!!"

# Getting the real-time temperature
def temp(city):
	API_ID = "[REDACTED]"
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_ID}"
	response = requests.get(url)

	if response.status_code == 200:
		data = response.json()
		temperature = data['main']['temp']
		return round(temperature-273.15,3)

	else: return "ERROR!!"
	
# Getting the articles and its urls
def list_of_articles(query):
	apiKey = "[REDACTED]"
	url = f"https://newsapi.org/v2/top-headlines?country={query}&apiKey={apiKey}"
	response = requests.get(url)

	if(response.status_code == 200):
		data = response.json()
		list_titles = []
		for i in range(10):
			title = (data['articles'][i]['title'], data['articles'][i]['url'])
			list_titles.append(title)
		return list_titles
	else: return "ERROR!!"

def open_url(url):
	"""Opens a URL in the user's browser"""

	webbrowser.open(url)
