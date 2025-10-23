from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import requests
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import base64
import requests


# Configuració del navegador
options = webdriver.FirefoxOptions()
options.add_argument("--start-maximized")
driver = webdriver.Firefox()
wait = WebDriverWait(driver, 20)


base_url = "https://litter.shinyapps.io/surfingforscience2/"
driver.get(base_url)
time.sleep(5)


# Tancar popup si apareix
try:
    dismiss_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Dismiss')]")))
    dismiss_button.click()
    print("Popup tancat.")
    time.sleep(2)
except:
    pass


# Trobar els punts del mapa
map_points = driver.find_elements(By.CLASS_NAME, "leaflet-interactive")
print(f"Ubicacions trobades: {len(map_points)}")

All_Data = driver.find_element(By.ID, "button_all")
print (All_Data)
All_Data.click()
time.sleep(4)

os.makedirs("ProjecteMicroplastics", exist_ok=True)
os.makedirs(r"ProjecteMicroplastics\Imatges", exist_ok=True)
# Obrir pestanya "Sample images"
sample_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sample images")))
sample_tab.click()
time.sleep(2)
# Esperar i canviar el select a "100"
try:
    select_element = wait.until(EC.presence_of_element_located((By.XPATH, '//* [starts-with (@name, "DataTables_")]')))
    select = Select(select_element)


    # Comprovem que l'opció "100" existeix
    options_text = [option.text for option in select.options]
    if "100" in options_text:
        select.select_by_visible_text("100")
        print("✅ Seleccionat 'Show 100 entries'")
        time.sleep(3)
    else:#
        print("⚠️ L'opció '100' no està disponible al select")
except Exception as e:
        print("❌ Error seleccionant 'Show 100 entries':", e)
#iframes = driver.find_elements(By.TAG_NAME, "iframe")
#print (iframes)
#print (f"\n S'han trobat {len(iframes)}")
#iframe = iframes.get_attribute('src')
#iframe_urls = []
#for iframe in iframes:
    #print(2)
    #id = iframe.get_attribute('id')
    #print (id)
#driver.switch_to.frame(iframe)
buttons = driver.find_elements(By.XPATH, "//*[contains(@class, 'paginate_button')]")
print (len(buttons))

for index, h in enumerate(buttons):
    Button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//*[@data-dt-idx='{index+8}']")))
    Button.click()
    print(f"\n Processant pagina {index + 1}")

    time.sleep(2)

    rows = driver.find_elements(By.XPATH, "//table//tbody//tr")

    print("S'han trobat ", len(rows), "files")

    for row in rows:
        # Primer número (canvia l'índex si no és la primera td)
        number1_td = row.find_element(By.XPATH, "./td[1]")
        number1 = number1_td.text.strip()

        # Imatge (canvia l'índex si no és la segona td)
        img_td = row.find_element(By.XPATH, "./td[2]")
        img = img_td.find_element(By.TAG_NAME, "img")
        src = img.get_attribute("src")
        img_url = urljoin(base_url, src)

        # Segon número (canvia l'índex si no és la tercera td)
        number2_td = row.find_element(By.XPATH, "./td[5]")
        number2 = number2_td.text.strip()

        # Combineu els dos números com vulgueu (amb guió baix per exemple)
        combined_numbers = f"{number1}_{number2}"

        filename = f"imatge_{combined_numbers}.jpg"
        path = os.path.join(r"ProjecteMicroplastics\Imatges", filename)

        try:
            r = requests.get(img_url)
            r.raise_for_status()
            with open(path, "wb") as f:
                f.write(r.content)
            print(f"Baixada imatge → {filename}")
        except Exception as e:
            print("Error baixant:", img_url, e)

           
#Parem el bucle
print ("Final del codi")
exit()
driver.quit()