import requests
import json

url = "http://127.0.0.1:5000/test"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers)
print(response.json())