import requests

url = "https://gilbra-bomalkt.hf.space/run/predict"
data = {"data": ["Test fake news"]}

response = requests.post(url, json=data)
print(response.json())  # Vérifier le retour API

input("\n")