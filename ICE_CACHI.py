from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime, timedelta

# Configurar el controlador de Selenium (aquí se usa Chrome)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Ejecutar en modo headless para no abrir la ventana del navegador
driver = webdriver.Chrome(options=options)

# URL de la página web
url = 'https://apps.grupoice.com/CenceWeb/CenceBoletinIntraDiario.jsf'

# Abrir la página web
driver.get(url)

# Esperar a que la página se cargue completamente
time.sleep(20)

# Crear listas para cada columna
data = []

# Rango de fechas (ajusta la fecha de inicio según sea necesario)
start_date = datetime.strptime("01/01/2023", "%d/%m/%Y")
end_date = datetime.strptime("31/12/2023", "%d/%m/%Y")
delta = timedelta(days=1)

current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%d/%m/%Y")
    
    # Encontrar el campo de fecha y establecer la fecha deseada
    date_field = driver.find_element(By.ID, 'j_id_12:pickFecha_input')
    date_field.clear()
    date_field.send_keys(date_str)
    date_field.send_keys(Keys.RETURN)

    # Esperar a que la página se actualice con los nuevos datos
    time.sleep(20)  # Ajustar este tiempo si es necesario

    # Verificar la tabla de datos actualizada
    rows = driver.find_elements(By.XPATH, '//tr[@role="row"]')
    
    # Recorrer las filas y extraer los datos específicos para "Cachí"
    for row in rows:
        cells = row.find_elements(By.XPATH, './/td[@role="gridcell"]')
        if len(cells) == 3:
            embalse_name = cells[0].text.strip()
            programado_value = cells[1].text.strip()
            real_value = cells[2].text.strip()
            
            if embalse_name == "Cachí":
                data.append({
                    'Fecha': date_str,
                    'Embalse': embalse_name,
                    'Programado (msnm)': programado_value,
                    'Real (msnm)': real_value
                })
                break  # Salir del bucle después de encontrar "Cachí"
    
    current_date += delta

# Cerrar el navegador
driver.quit()

# Crear un DataFrame con los datos extraídos
df = pd.DataFrame(data)

# Guardar el DataFrame en un archivo CSV 
csv_path = 'C:/Users/jose_/Documents/Gaby/cence_data_2024_1.csv'
df.to_csv(csv_path, index=False)

print(f"Datos guardados en '{csv_path}'")
