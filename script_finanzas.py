from bs4 import BeautifulSoup
import requests
import datetime
import pandas as pd
import os

print("Inicio del script...")

url = r"https://es.finance.yahoo.com/mercados/acciones/subidas/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
respuesta = requests.get(url, headers=headers)
if respuesta.status_code == 200:#comprobamos la respuesta, si es 200 todo ha ido ok
    soup = BeautifulSoup(respuesta.content, "html.parser")
    time = datetime.datetime.now().strftime("%Y-%m-%d")
else:
    print("No se ha recolectado nada.")

get_ids = soup.find_all('tr', id=True)

for ids in get_ids:
    ids.get('id')

max_ids = int(ids.get('id'))

saved_data = []

for num in range(max_ids+1):
    table = soup.find('tr', id=num)
    
    symbol = table.select('td')[0].get_text().strip()
    name = table.select('td')[1].get_text().strip()
    price = table.select('fin-streamer')[0].get_text().replace(",", ".")
    change = table.select('td')[5].get_text().strip().replace(",", ".").replace("+", "")
    volume = table.select('td')[6].get_text().strip().replace(",", "").replace(".", "")
        
    if 'M' in volume:
        volume = volume.replace("M", "").replace(",",".")
        volume = round(float(volume) * 1000000)
    else:
        volume = volume.replace(".", "")
        
    saved_data.append([time, symbol, name, float(price), change, int(volume)])
    
column_names = ["Fecha", "Simbolo", "Nombre", "Precio", "Cambio", "Volumen"]

df = pd.DataFrame(saved_data, columns=column_names)

path = os.path.abspath("./mejores_subidas")

if not os.path.exists(path):
    print(f"Creando carpeta en: {path}")
    os.makedirs(path)
    
full_path = os.path.join(path, f"subidas_acciones_{time}.csv")

df.to_csv(full_path, encoding='utf-8-sig', index=False) #El encode es necesario para tildes y caracteres más concretos del español.

print("Fin del script.")