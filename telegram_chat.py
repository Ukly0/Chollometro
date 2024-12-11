
import cv2
import numpy as np
import openpyxl
from PIL import ImageFont, ImageDraw, Image  
import textwrap
import telebot
from base64 import b64encode
from imagekitio import ImageKit
import nltk
import re
from nltk.corpus import stopwords
import time

nltk.download('punkt')

IK_PUBLIC = "public_qrreRhsOiHJvMLm2t3VQ5lrhLUM="
IK_PRIVATE = "private_EcZ9w9Z6yZL9Vk2VMEwV/3DF10I="
IK_URL = "https://ik.imagekit.io/ukly0"

TOKEN = '5956361099:AAF9aRLImw4KrrWgBfBIMmNxwdeu4lNdjRA'
bot = telebot.TeleBot(TOKEN)
chat_id = '-1001693078387'

nuevo_archivo = 'nuevos_chollos.xlsx'

ik = ImageKit(public_key=IK_PUBLIC, private_key= IK_PRIVATE, url_endpoint=IK_URL)
datos = []
datos_archivo = 'nuevos_chollos.xlsx'

def leer_archivo():
    # Cargar el libro de Excel
    datos_excel = openpyxl.load_workbook(datos_archivo)

    # Obtener la hoja de trabajo activa
    historico_hoja_trabajo = datos_excel.active

    # Recorrer las filas de la hoja de trabajo y leer los datos
    for fila in historico_hoja_trabajo.iter_rows(min_row=2, values_only=True):
        titulo, link, precio_original, precio, imagen, id, id_producto = fila
        datos.append([titulo, link, precio_original, precio, imagen, id, id_producto])

# Crear un nuevo libro de Excel y seleccionar la hoja de trabajo activa
def redimensionar_imagen(imagen, nuevo_ancho, nuevo_alto,id):
    img = Image.open(imagen)
    img.thumbnail((nuevo_ancho, nuevo_alto))
    img.save(f"Imagenes/{id}.jpg")  # Guardar la imagen redimensionada en un archivo
    


def ik_subir_imagen(id):
    with open('Ofertas/'+id+".jpg", "rb") as f:
        imagen = b64encode(f.read())
    print("subiendo imagen a imagekit")
    try: 
        res = ik.upload_file(file=imagen, file_name="id.jpg")
    except Exception as e:
        return f'ERROR: {e}'
    status_code=res.response_metadata.http_status_code

    if status_code == 200:
        return res.response_metadata.raw
 
def enviar_mensaje(titulo,link,precio_anterior,precio,id_foto):

    print(f'El mensaje tiene {len(titulo)} caracteres')
    url_foto = ik_subir_imagen(id_foto).get("url")
    
    if precio_anterior != "0":

        precio_anterior=precio_anterior.replace(",",".")
        precio=precio.replace(",",".")

        precio_anterior = re.sub(r'[^\d.]', '', precio_anterior)
        precio = re.sub(r'[^\d.]', '', precio)
        
        try:
            precio_anterior = float(precio_anterior)
            precio = float(precio)
        except ValueError:
            print("Error: El valor ingresado no es un número válido.")
        diferencia = precio_anterior - precio
        porcentaje_rebaja = round((diferencia / precio_anterior) * 100)

        mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕ AHORRAS UN <b> {porcentaje_rebaja}% </b>⭕\n\n🔖 {titulo} \n\n 🔰 <a href="{link}">Enlace de compra</a> \n\n @amazonoferta_es'
    
    else:
        mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕¡Nuevo Descuento Encontrado!⭕\n\n🔖 {titulo} \n\n 🔰<a href="{link}">Enlace de compra</a>\n\n @amazonoferta_es'
    
    
    bot.send_message(chat_id,mensaje,parse_mode="html")

def crear_imagen(titulo,precio_oferta,precio,id):

    # Descargar el paquete de stopwords en español
    nltk.download('stopwords')

    # Obtener las palabras de parada en español
    stopwords_es = set(stopwords.words('spanish'))

    # Definir la oración de entrada
    oracion = titulo

    # Tokenizar la oración en palabras
    palabras = nltk.word_tokenize(oracion)

    # Filtrar las palabras de parada
    palabras_filtradas = [palabra for palabra in palabras if palabra.lower() not in stopwords_es]

    # Obtener las dos primeras palabras
    titulo = palabras_filtradas[:2]

    width = 1140
    height = 720

    imagen_original = f'Imagenes/{id}.jpg'
    ancho_deseado = 800
    alto_deseado = 1000

    overlay_image = cv2.imread(imagen_original)
    overlay_image = cv2.resize(overlay_image, (470, 470))

    # Crear una imagen blanca
    #image = np.ones((height, width, 3), dtype=np.uint8) * 255  # Matriz llena de 255 (blanco)
    image = cv2.imread("chollo.png")

    # Superponer la imagen en el margen izquierdo
    x_offset = 50  # Margen izquierdo
    y_offset = 80  # Margen superior
    image[y_offset:y_offset + overlay_image.shape[0], x_offset:x_offset + overlay_image.shape[1]] = overlay_image

    # Convertir la imagen a formato PIL.Image
    pil_image = Image.fromarray(image)

    # Crear un objeto ImageDraw para dibujar en la imagen
    draw = ImageDraw.Draw(pil_image)

    # Cargar la fuente personalizada
    font_path = "Fuente/Amazon.otf"  # Reemplaza con la ruta de tu fuente personalizada
    font_size = 80
    font = ImageFont.truetype(font_path, font_size)

    # Configurar el texto
    text = " ".join(titulo)

    # Dividir el texto en líneas para ajustarlo a la imagen
    text_lines = textwrap.wrap(text, width=10)  # Cambia el valor de width según tus necesidades

    # Escribir el texto en la imagen utilizando la fuente personalizada
    text_position = (width/2, 70)
    text_color = (225,168,0)  # Color del texto en formato RGB (negro en este caso)
    line_height = font.getsize(text_lines[0])[1] + 4  # Espacio entre líneas

    total_height = line_height * len(text_lines)

    text_y = (height - total_height) // 6

    for line in text_lines:
        text_width, text_height = font.getsize(line)
        text_x = (width*1.5 - text_width) // 2
        text_position = (text_x, text_y)
        draw.text(text_position, line, font=font, fill=text_color)
        text_y += line_height

    font_path = "Fuente/Amazon.otf"  # Reemplaza con la ruta de tu fuente personalizada
    font_size = 90
    font = ImageFont.truetype(font_path, font_size)
    text_color = (255,255,255)
    # Configurar el segundo texto
    
    # Dividir el segundo texto en líneas para ajustarlo a la imagen
    text_lines2 = textwrap.wrap(precio, width=15)  # Cambia el valor de width según tus necesidades

    # Calcular la altura total del segundo texto
    line_height = font.getsize(text_lines2[0])[1] + 4  # Espacio entre líneas
    total_height = line_height * len(text_lines2)

    # Calcular la posición de inicio del segundo texto debajo del primer texto
    text_y = 315

    # Escribir el segundo texto en la imagen utilizando la fuente personalizada
    for line in text_lines2:
        text_width, text_height = font.getsize(line)
        text_x = (width*1.5 - text_width) // 2
        text_position = (text_x, text_y)
        draw.text(text_position, line, font=font, fill=text_color)
        
    if precio_oferta != "0":
        # Dividir el tercer texto en líneas para ajustarlo a la imagen
        text_lines3 = textwrap.wrap(precio_oferta, width=30)  # Cambia el valor de width según tus necesidades

        # Calcular la altura total del tercer texto
        line_height = font.getsize(text_lines3[0])[1] + 4  # Espacio entre líneas
        total_height = line_height * len(text_lines3)

        # Calcular la posición de inicio del tercer texto debajo del segundo texto
        text_y = 450

        # Escribir el tercer texto en la imagen utilizando la fuente personalizada
        text_color3 = (155, 155, 155)  # Color azul en formato RGB

        font_path = "Fuente/Amazon.otf"  # Reemplaza con la ruta de tu fuente personalizada
        font_size = 80
        font = ImageFont.truetype(font_path, font_size)

        for line in text_lines3:
            text_width, text_height = font.getsize(line)
            text_x = (width*1.5 - text_width) // 2
            text_position = (text_x, text_y)
            draw.text(text_position, line, font=font, fill=text_color3)
            text_y += line_height

        line_y = text_y - line_height // 1.7
        line_start = (text_x, line_y)
        line_end = (text_x + text_width, line_y)

        # Dibujar la línea de tachado
        draw.line([line_start, line_end], fill=text_color3, width=6)

        # Convertir la imagen PIL.Image de vuelta a formato NumPy
   
    result_image = np.array(pil_image)
    output_path = f"Ofertas/{id}.jpg"

    cv2.imwrite(output_path, result_image)

    # Mostrar la imagen resultante en una ventana
    #cv2.imshow("Imagen", result_image)
    #cv2.destroyAllWindows()


def main():
    leer_archivo()
    for d in datos:
        time.sleep(10)
        crear_imagen(d[0],d[2],d[3],d[5])
        enviar_mensaje(d[0],d[1],d[2],d[3],d[5])
        datos.remove(d)
    
