import requests
API_KEY = "ba1ed707c9424dbeae869e88e45ad9ae"
url = "https://newsapi.org/v2/everything"
params = {
    "q": "Apple",
    "from": "2026-01-16",
    "sortBy": "popularity",
    "apiKey": API_KEY
}

response = requests.get(url, params=params)
