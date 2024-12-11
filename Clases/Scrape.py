# Configura tus credenciales de Firebase
import time
import random
import requests
import openpyxl
import time
import random
import os
import requests
import re
import ConstantesChollometro as ConstantesChollometro
import OfertasDao as OfertasDao

from Oferta import Oferta
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime


urls = [
        'https://www.chollometro.com/populares',
        'https://www.chollometro.com/',
        'https://www.chollometro.com/categorias/libros',
        'https://www.chollometro.com/categorias/videojuegos',
        'https://www.chollometro.com/categorias/salud-y-cosmeticos',
        'https://www.chollometro.com/categorias/figuras',
        'https://www.chollometro.com/categorias/naturaleza-y-deportes-de-invierno'
    ]

# URL de la página web
webdriver_service = Service('chromedriver.exe') # Ruta del controlador del navegador (ejemplo para Chrome)
delay_min = 5
delay_max = 15
retardo = random.uniform(delay_min, delay_max)
db = OfertasDao.db #Definimos el acceso a la base de datos


def es_imagen(url):

    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        image = Image.open(response.raw)
        image.verify()
        
        return True
    except (requests.exceptions.RequestException, IOError, Image.DecompressionBombError):
        return False


def seleccionar_url(id_producto,imagenchollo):

    url500 = f'https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=ES&ASIN={id_producto}&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=SL500'
    url250 = f'https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=ES&ASIN={id_producto}&ServiceVersion=20070822&ID=AsinImage&WS=1&Format=SL250'
    url = f'https://ws-eu.amazon-adsystem.com/widgets/q?_encoding=UTF8&MarketPlace=ES&ASIN={id_producto}&ServiceVersion=20070822&ID=AsinImage&WS=1&'
    
    
    if es_imagen(url500):
        return requests.head(url500,allow_redirects=True).url
    if es_imagen(imagenchollo):
        return requests.head(imagenchollo,allow_redirects=True).url
    if es_imagen(url250):
        return requests.head(url250,allow_redirects=True).url
    if es_imagen(url):
        return requests.head(url,allow_redirects=True).url
    else:
        print("Imagen no valida")
        return None
    

def chollometro_scrape(soup,categoria):
    # Buscar todos los elementos que contengan la clase deseada
    elements = soup.find_all(class_= ConstantesChollometro.OFERTAS)
    # Recorrer e imprimir los elementos encontrados
    for element in elements :

        print('......... FILTRANDO OFERTA  .........')

        titulo = element.find(class_= ConstantesChollometro.TITULO).find('a').text
        print(titulo)
        linkid = element.find(class_= ConstantesChollometro.ENLACE)['href']
        imagenchollo = element.find(class_=ConstantesChollometro.IMAGEN)['src']
        tienda = element.find(class_= ConstantesChollometro.TIENDA)
        precio = element.find(class_ = ConstantesChollometro.PRECIO)
        
        warm = element.find(class_ = 'cept-vote-temp vote-temp vote-temp--warm')
        hot = element.find(class_ = 'cept-vote-temp vote-temp vote-temp--hot')
        burn = element.find(class_ = 'cept-vote-temp vote-temp vote-temp--burn')

        if tienda and tienda.text == "Amazon" and titulo and precio and (warm or hot or burn):
            print('++++++++ OFERTA ENCONTRADA +++++++++')
            precio = element.find(class_ = ConstantesChollometro.PRECIO).text
            temperatura = element.find(class_= 'flex boxAlign-ai--all-c boxAlign-jc--all-sb space--b-3 space--fromW3-b-2').find('span').text
            temperatura = int(temperatura.replace("°", ""))


            #img = element.find(class_ = ConstantesChollometro.IMAGEN)['src']
            id= linkid.rsplit("-", 1)[-1]

            if element.find(class_ = ConstantesChollometro.PRECIO_ORIGINAL) is not None:
                precio_original = element.find(class_ = ConstantesChollometro.PRECIO_ORIGINAL ).text
            else:
                precio_original = "0"
            
            #Tratamiento del enlace
            link = requests.get('https://www.chollometro.com/visit/threadmain/'+id)
            linkAmazon = link.url
            linkafiliado_y_producto = get_linkAfiliado(linkAmazon)
            if linkafiliado_y_producto:
                linkAfiliado,id_Producto = linkafiliado_y_producto
            else:
                linkAfiliado,id_Producto = None, None
            url_img = seleccionar_url(id_Producto,imagenchollo)

            if url_img:
                img = url_img
            else:
                img = None
           

            if(id_Producto is not None and linkAfiliado is not None and img is not None): 
                #guardar_imagen(id,img)
                try:
                    #image = Image.open(os.path.join("Imagenes", id+".jpg"))
                    #image.verify()

                    oferta = Oferta(
                        titulo=titulo,
                        link_afiliado=linkAfiliado,
                        precio_original=precio_original,
                        precio=precio,
                        img=img,
                        oferta_id=id,
                        producto_id=id_Producto,
                        categoria=categoria
                    )

                    oferta.toString()

                    oferta.insertar_oferta(db)

                except (requests.exceptions.RequestException, IOError, Image.DecompressionBombError):
                    # La imagen no es válida
                    # Eliminar la imagen
                    os.remove(os.path.join("Imagenes", id+".jpg"))
                    print("La imagen no es válida. No se insertó la oferta y se eliminó la imagen.")

        else:
            print(f"NO SE ENCUENTRA ID_PRODUCTO O LINKAFILIADO ")


def get_linkAfiliado(linkAmazon):
    linkAfiliado = ""
    id_Producto_match = re.search(r'(?:dp/([\w]*))|(?:gp/product/([\w]*))', linkAmazon.split(" ")[0])
    
    if id_Producto_match is not None:

        if id_Producto_match.group(1):
            id_Producto = id_Producto_match.group(1)
        else:
            id_Producto = id_Producto_match.group(2)

        linkAfiliado = f"https://www.amazon.es/dp/{id_Producto}?th=1&psc=1&linkCode=ll1&tag=ukly008-21&ref_=as_li_ss_tl"
        if id_Producto is not None:

            return linkAfiliado,id_Producto
        else:
            return None

    else:
        print("---- ID DE PRODUCTO NO ENCONTRADO EN AMAZON")
        return None

    

def get_categoria_from_url(url):
    match = re.search(r"/([-\w]+)(?<!-)$", url)
    if (match is None or match.group(1) == "populares"):
        categoria = "todo"
    else:
        categoria = match.group(1)

    print(f"\n@@@@@@@@@@@ {categoria} @@@@@@@@@@@ ")
    return  categoria

def guardar_imagen(id, img):
    ruta_archivo = os.path.join("Imagenes", id+".jpg")
    response = requests.get(img)

    with open(ruta_archivo, "wb") as archivo:
        archivo.write(response.content)

def scrape():
    
    # Configuración del controlador del navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Ejecutar en modo sin cabeza (sin interfaz gráfica)
    options.add_argument('--no-sandbox')
    

    for url in urls:
        time.sleep(10)
        driver = webdriver.Edge()
        #driver = webdriver.Chrome(service=webdriver_service, options=options)
        # Cargar la página
        driver.get(url)

        categoria = get_categoria_from_url(url)

        # Definir la función de desplazamiento mediante JavaScript
        def scroll_to_bottom():
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Realizar el desplazamiento hasta que no haya más contenido cargado
        while True:
            # Obtener el contenido actualizado después del desplazamiento
            updated_content = driver.page_source
            # Desplazarse hasta el final de la página
            scroll_to_bottom()
            # Esperar a que se cargue el nuevo contenido
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//footer")))
            # Verificar si se ha llegado al final de la página
            if updated_content == driver.page_source:
                break

        # Cerrar el controlador del navegador
        driver.quit()

        # Crear el objeto BeautifulSoup con el contenido actualizado
        soup = BeautifulSoup(updated_content, 'html.parser')

        chollometro_scrape(soup,categoria)

        
          