import requests

url = "https://coop-land.ru/helpguides/new/"

response = requests.get(url)
response.raise_for_status()
print(response.text)