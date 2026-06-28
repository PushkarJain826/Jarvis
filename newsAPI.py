import requests
import dotenv

dotenv.load_dotenv()
API_KEY = dotenv.get_key(".env", "NEWS_API_KEY")
url = "https://newsapi.org/v2/everything"
params = {
    "q": "Apple",
    "from": "2026-01-16",
    "sortBy": "popularity",
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
