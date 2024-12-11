import time
import random
import requests
import openpyxl
import time
import random
import os
import requests
import re
import selenium.webdriver

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as E
import time

webdriver_service = Service('chromedriver.exe') # Ruta del controlador del navegador (ejemplo para Chrome)
delay_min = 5
delay_max = 15
retardo = random.uniform(delay_min, delay_max)
driver = webdriver.Edge()

webdriver_service = Service('chromedriver.exe')
url = [
        'https://www.chollometro.com/populares',
        'https://www.chollometro.com/',
        'https://www.chollometro.com/categorias/libros',
        'https://www.chollometro.com/categorias/videojuegos',
        'https://www.chollometro.com/categorias/salud-y-cosmeticos',
        'https://www.chollometro.com/categorias/figuras',
        'https://www.chollometro.com/categorias/naturaleza-y-deportes-de-invierno'
    ]
driver.get(url[0])
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Navegar a la página web con scroll infinito
        #driver = webdriver.Chrome(service=webdriver_service, options=options)
        # Cargar la página

# Definir la cantidad de desplazamiento y la espera entre desplazamientos
scroll_amount = 3  # Cambia esto según tu preferencia
scroll_wait = 1.5   # Cambia esto según tu preferencia

# Encontrar el botón por su clase
button_class_cookies = "overflow--wrap-on flex--grow-1 flex--fromW3-grow-0 width--fromW3-ctrl-m space--mb-3 space--fromW3-mb-0 space--fromW3-mr-2 button button--shape-circle button--type-primary button--mode-brand"
button = driver.find_element("xpath", "//button[text()=' Aceptar todo ']")

button.click();

WebDriverWait(driver, 10)
button = driver.find_element("xpath", "//button[contains(@class, 'button--toW5-square space--ml-2 button button--shape-circle button--type-primary button--mode-white')]")

#button = driver.find_element(By.CLASS_NAME, "button--toW5-square space--ml-2 button button--shape-circle button--type-primary button--mode-white")
print(button)
button.click()
driver.implicitly_wait(5)
usuario = driver.find_element(By.ID, 'loginModalForm-identity')
usuario.send_keys("aeg.expositogarcia@gmail.com")

contraseña = driver.find_element(By.ID, 'loginModalForm-password')
contraseña.send_keys("13isejeC")

button = driver.find_element("xpath", "//button[text()='Inicia sesión']")
button.click()

reached_page_end = False

# Función para simular el desplazamiento gradual
def scroll_down():
    actions = ActionChains(driver)
    for _ in range(scroll_amount):
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        time.sleep(scroll_wait)

def clickreno():
    try:

        breno = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button button--type-primary button--mode-white button--shape-circle text--upper width--all-12"))
        )
        #encontrado = driver.find_element(By.CLASS_NAME, 'button button--type-primary button--mode-white button--shape-circle text--upper width--all-12')
        print(breno)
        if breno:
            print("Encontradooooooo")
            breno.click()
            return True
        else:
            print("No encontrado")
            return False
    except:
         print("Excepcion: No encontrado")


# Realizar el desplazamiento gradual
try:
    reno = False
    pagina = 0;
    while not reno:
        last_height = driver.execute_script("return document.body.scrollHeight")
        final = False
        while not final:
            scroll_down()
            reno = clickreno()
            new_height = driver.execute_script("return document.body.scrollHeight")
            if last_height == new_height:
                print("Entro")
                scroll_down()
                reno = clickreno()
                scroll_down()
                last_height = driver.execute_script("return document.body.scrollHeight")
                if last_height == new_height:
                    reno = clickreno()
                    pagina = pagina + 1
                    n = pagina % 6;
                    final = True
                    print("Final")
                    driver.get(url[n])
            else:
                last_height = driver.execute_script("return document.body.scrollHeight")
            
    
except KeyboardInterrupt:
    # Detener el desplazamiento si se presiona Ctrl+C
    pass

# Cerrar el navegador al final
driver.quit()