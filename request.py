import requests

url = 'http://localhost:5000/predict_api'
r = requests.post(url, json={'Age':20, 'Sex':'Laki-laki', 'Smoker':'Tidak'})

print(r.json())