import nltk
import textwrap
import cv2
import numpy as np
import string
import os
import requests
import OfertasDao
import time
from Oferta import Oferta
from imagekitio import ImageKit
from nltk.corpus import stopwords
# version 9.5 el getsize() se elimina en las siguiente actualizaciones
from PIL import ImageFont, ImageDraw, Image  
from base64 import b64encode
from imagekitio import ImageKit

IK_PUBLIC = "public_qrreRhsOiHJvMLm2t3VQ5lrhLUM="
IK_PRIVATE = "private_EcZ9w9Z6yZL9Vk2VMEwV/3DF10I="
IK_URL = "https://ik.imagekit.io/ukly0"
IMAGEN_BASE = "chollosjuego.jpg"
IMAGEN_AGOTADO = 'agotado.png'
FUENTE = os.path.join("Fuente", "Amazon.otf")
FUENTE_PRECIO = os.path.join("Fuente", "Poppins-ExtraBold.ttf")
FUENTE_PRECIO_SIZE = 175
FUENTE_TITULO = os.path.join("Fuente", "Futura-Bold.otf")
FUENTE_TITULO_SIZE_ = 45
FUENTE_AHORRAS = os.path.join("Fuente", "Poppins-Light.ttf")
FUENTE_AHORRAS_SIZE = 30
FUENTE_PRECIO_AHORRAS_SIZE = 32


NEGRO = (0,0,0)
BLANCO = (255,255,255)

X_TITULO = 400
Y_TITULO = 220

Y_PRECIO = 340

Y_AHORRAS = 600
Y_AHORRASP = 598

X_AHORRASPR = 832
X_AHORRASP = 1110

color_acento = NEGRO

ik = ImageKit(public_key=IK_PUBLIC, private_key= IK_PRIVATE, url_endpoint=IK_URL)

db = OfertasDao.db

nltk.download('stopwords')
def obtener_variantes_categoria(categoria):
    if categoria == "todo":
        return "chollosamazon.jpg", hex_to_bgr('#698ed2')
    elif categoria == "libros":
        return "chollosebook.jpg", hex_to_bgr('#477876')
    elif categoria == "videojuegos":
        return "chollosjuego.jpg", hex_to_bgr('#e76f51')
    elif categoria == "figuras":
        return "chollosfiguras.jpg", hex_to_bgr('#04b38d')
    elif categoria == "salud-y-cosmeticos":
        return "chollossalud.jpg", hex_to_bgr('#f0cf6e')
    elif categoria == "naturaleza-y-deportes-de-invierno":
        return "cholloscampings.jpg", hex_to_bgr('#52cc5e')
    # Agrega más condiciones para cada categoría que tengas

import os
import requests

def guardar_imagen(id, img):
    ruta_archivo = os.path.join("Imagenes", id + ".jpg")
    response = requests.get(img)

    try:
        response.raise_for_status()  # Verifica si hay errores en la solicitud
        with open(ruta_archivo, "wb") as archivo:
            archivo.write(response.content)
        print("Imagen guardada exitosamente")
    except requests.exceptions.HTTPError as errh:
        print("Error HTTP:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error de conexión:", errc)
    except requests.exceptions.Timeout as errt:
        print("Error de tiempo de espera:", errt)
    except requests.exceptions.RequestException as err:
        print("Error en la solicitud:", err)


def agotado_crear(id):
    imagen = cv2.imread(os.path.join("Ofertas", f"{id}.jpg"))


    if imagen is None:
        print("Error al cargar la imagen.")
    else:
        # Obtener dimensiones de la imagen
        alto, ancho, _ = imagen.shape

        # Crear una imagen en blanco para el rectángulo
        rectangulo = imagen.copy()

        # Definir márgenes en alto y ancho
        margen_alto = int(alto // 1.5)
        margen_ancho = ancho // 6

        # Calcular coordenadas del rectángulo centrado con los márgenes
        x_inicio = margen_ancho
        y_inicio = margen_alto
        x_fin = ancho - margen_ancho
        y_fin = alto - margen_alto

        # Dibujar el rectángulo negro con bordes redondeados y transparencia
        cv2.rectangle(rectangulo, (x_inicio, y_inicio), (x_fin, y_fin), (0, 0, 0), -1)
        cv2.addWeighted(imagen, 0.2, rectangulo, 0.7, 0, imagen)

        # Agregar el texto "Agotado" en el centro del rectángulo con fuente personalizada y color RGB
        texto = 'Agotado'
        ruta_fuente = FUENTE_PRECIO  # Reemplaza con la ruta de tu archivo TTF
        fuente_pil = ImageFont.truetype(ruta_fuente, FUENTE_PRECIO_SIZE)
        imagen_pil = Image.fromarray(imagen)
        draw = ImageDraw.Draw(imagen_pil)
        color_rgb = (255, 255, 255)  # Cambiar a tu color RGB deseado
        texto_ancho, texto_alto = draw.textsize(texto, font=fuente_pil)
        texto_x = x_inicio + (x_fin - x_inicio - texto_ancho) // 2
        texto_y = (alto - texto_alto) // 2
        draw.text((texto_x, texto_y), texto, font=fuente_pil, fill=color_rgb)

        imagen = np.array(imagen_pil)

        # Mostrar la imagen resultante
        #cv2.imshow('Imagen con Rectángulo Negro Transparente y Texto', imagen)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()

        output_path = f"Ofertas/{id}.jpg"

        cv2.imwrite(output_path, imagen)

def ik_subir_imagen(oferta):
    
    imagen_creada = crear_imagen(oferta)
   
    if imagen_creada:
        imagen = os.path.join("Ofertas", oferta.oferta_id+".jpg")
        with open(imagen, "rb") as f:
            imagen = b64encode(f.read())
        try: 
            res = ik.upload_file(file=imagen, file_name="id.jpg")
            print("\tImagen subida")
        except Exception as e:
            return f'ERROR: {e}'
        status_code=res.response_metadata.http_status_code

        if status_code == 200:
            return res.response_metadata.raw
    else: 
        return None
        print('No se pudo crear')
    
def ik_actualizar_imagen(oferta):
    agotado_crear(oferta.get("oferta_id"))
    imagen = os.path.join("Ofertas", oferta.get("oferta_id")+".jpg")
    with open(imagen, "rb") as f:
        imagen = b64encode(f.read())
    try: 
        res = ik.upload_file(file=imagen, file_name="id.jpg")
        print("\tImagen subida")
    except Exception as e:
        return f'ERROR: {e}'
    status_code=res.response_metadata.http_status_code

    if status_code == 200:
        return res.response_metadata.raw




def hex_to_bgr(hex_code):

    # Remove the '#' symbol if present
    hex_code = hex_code.lstrip('#')
     # Convert the hexadecimal code to BGR
    bgr = tuple(int(hex_code[i:i+2], 16) for i in (4, 2, 0))
    return bgr


def crear_titulo(titulo):
    # Descargar el paquete de stopwords en español
    # Obtener las palabras de parada en español
    stopwords_es = set(stopwords.words('spanish'))
    # Obtener los signos de puntuación
    signos_puntuacion = set(string.punctuation)
    # Definir la oración de entrada
    oracion = titulo
    # Tokenizar la oración en palabras
    palabras = nltk.word_tokenize(oracion)
    # Filtrar las palabras de parada y los signos de puntuación
    palabras_filtradas = [palabra for palabra in palabras 
                          if palabra.lower() not in stopwords_es 
                          and palabra not in signos_puntuacion 
                          and not palabra.isdigit()]
    # Obtener las dos primeras palabras
    resultado = palabras_filtradas[:2]
    
    return resultado

def redondeo_decimal(numero):
    parte_entera = int(numero)  # Obtiene la parte entera del número
    parte_decimal = round(numero - parte_entera, 1)  # Obtiene la parte decimal redondeada a 1 decimal

    #print(f'Parte decimal: {parte_decimal}')
    #print(f'Parte entera: {parte_decimal}')
    
    if len(str(parte_entera)) < 2 and parte_decimal != 0:
        print(float(f"{parte_entera}.{str(parte_decimal)[2]}"))
        return float(f"{parte_entera}.{str(parte_decimal)[2]}")  # Devuelve la parte entera y el primer decimal como float
    else:
        return parte_entera  # Devuelve la parte entera si tiene 2 o más dígitos o si el decimal es cero

def crear_imagen(oferta):

    titulo = crear_titulo(oferta.titulo)
    precio_oferta = str(redondeo_decimal(float(oferta.precio_original)))
    porcentaje = str(float(oferta.porcentaje))
    precio = str(redondeo_decimal(float(oferta.precio)))

    IMAGEN_BASE,color_acento = obtener_variantes_categoria(oferta.categoria)
    id = oferta.oferta_id
    
    fuente_precio = ImageFont.truetype(FUENTE_PRECIO, FUENTE_PRECIO_SIZE)
    fuente_titulo = ImageFont.truetype(FUENTE_TITULO, FUENTE_TITULO_SIZE_)
    guardar_imagen(id,oferta.img)
    time.sleep(5)
    #Cargamos imagen
    imagen = os.path.join("Imagenes", id+".jpg")
    image = cv2.imread(IMAGEN_BASE)

    alto_imagen, ancho_imagen, _ = image.shape

    print(id)

    imagen_producto = cv2.imread(imagen)

    if imagen_producto is not None:
        alto_producto, ancho_producto, _ = imagen_producto.shape
    
        alto_producto, ancho_producto, _ = imagen_producto.shape
        # Calcular el factor de escala para mantener la relación de aspecto
        if ancho_producto > alto_producto:
            factor_escala = 550 / ancho_producto
        else:
            factor_escala = 550 / alto_producto
        
        # Redimensionar la imagen manteniendo la relación de aspecto
        ancho_producto = int(ancho_producto * factor_escala)
        alto_producto = int(alto_producto * factor_escala)

        imagen_producto = cv2.resize(imagen_producto, (ancho_producto, alto_producto))

        x_distancia = int(ancho_imagen * 0.25) - int(ancho_producto/2)  # Posición x en el lado izquierdo (ajustable según necesidad)
        y_distancia = int((alto_imagen - alto_producto) / 2) + 30  # Posición y en el centro vertical

        image[y_distancia:y_distancia+alto_producto, x_distancia:x_distancia+ancho_producto] = imagen_producto

        # Convertir la imagen a formato PIL.Image
        pil_image = Image.fromarray(image)

        # Crear un objeto ImageDraw para dibujar en la imagen
        draw = ImageDraw.Draw(pil_image)

        titulo = " ".join(titulo).upper()
        print(titulo)
        # Escribir el texto en la imagen utilizando la fuente personalizada

        titulo_ancho, _ = fuente_titulo.getsize(titulo)
        x_titulo = ((ancho_imagen*1.5 - titulo_ancho)//2) - 10

        titulo_position = (x_titulo, Y_TITULO)
        draw.text(titulo_position, titulo, font=fuente_titulo, fill=color_acento)

        # Configurar el PRECIO
        precio = (str(precio)+'€').upper()


        text_width = draw.textsize(precio, font=fuente_precio)[0]
        x_precio = ((ancho_imagen*1.5 - text_width)//2) - 10

        text_position = (x_precio, Y_PRECIO)
        draw.text(text_position, precio, font=fuente_precio, fill=BLANCO)

            
        if precio_oferta != "0":
                
                fuente_ahorras = ImageFont.truetype(FUENTE_AHORRAS, FUENTE_AHORRAS_SIZE)

                ahorras = ("[ANTES A            AHORRAS UN           ]").upper()
                ahorras_ancho = draw.textsize(ahorras, font=fuente_ahorras)[0]
                x_ahorras = ((ancho_imagen*1.5 - ahorras_ancho)//2) - 10
                text_position = (x_ahorras, Y_AHORRAS)

                draw.text(text_position, ahorras, font=fuente_ahorras, fill=color_acento)
                #--------------------------------------- PRECIO ORIGINAL

                fuente_porcentaje = ImageFont.truetype(FUENTE_PRECIO, FUENTE_AHORRAS_SIZE)

                precio_ori = (str(int(float(precio_oferta)))+'€').upper()
                #precio_ori_ancho = draw.textsize(precio_ori, font=fuente_porcentaje)[0]
                precio_ori_position = (X_AHORRASPR, Y_AHORRASP)
                draw.text(precio_ori_position, precio_ori, font=fuente_porcentaje, fill=NEGRO)

                #--------------------------------------- PORCENTAJE
                porcentaje = (str(int(float(porcentaje)))+'%').upper()
                porcentaje_position = (X_AHORRASP, Y_AHORRASP)
                draw.text(porcentaje_position, porcentaje, font=fuente_porcentaje, fill=NEGRO)


        result_image = np.array(pil_image)
        output_path = f"Ofertas/{id}.jpg"

        cv2.imwrite(output_path, result_image)
        os.remove(os.path.join("Imagenes", id+".jpg"))
        return True
        
    else:
        print("Error: La imagen no se cargó correctamente.")
        os.remove(os.path.join("Imagenes", id+".jpg"))
        return False

    # Mostrar la imagen resultante en una ventana
    #cv2.imshow("Imagen", result_image)
    #cv2.destroyAllWindows()

