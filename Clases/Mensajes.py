
import numpy as np
import nltk
import telebot
import datetime
import OfertasDao
import Imagenes
import time
from Oferta import Oferta
from nltk.corpus import stopwords
#version 9.5 el getsize() se elimina en las siguiente actualizaciones
from PIL import ImageFont, ImageDraw, Image  
from base64 import b64encode
from imagekitio import ImageKit


nltk.download('punkt')

IK_PUBLIC = "public_qrreRhsOiHJvMLm2t3VQ5lrhLUM="
IK_PRIVATE = "private_EcZ9w9Z6yZL9Vk2VMEwV/3DF10I="
IK_URL = "https://ik.imagekit.io/ukly0"

TOKEN = '5956361099:AAF9aRLImw4KrrWgBfBIMmNxwdeu4lNdjRA'
bot = telebot.TeleBot(TOKEN)

CHAT_TODOS = '-1001693078387'
CHAT_EBOOK = '-1001845184249'
CHAT_FIGURAS = '-1001845512659'
CHAT_JUEGOS = '-1001671836804'
CHAT_SALUD = '-1001805624917'
CHAT_CAMPING = '-1001638909546'

db = OfertasDao.db 

def leer_archivo():
    return Oferta.obtener_ofertas_nuevas(db)

def enviar_mensaje():
        ofertas = leer_archivo()
        for oferta_key, oferta_info in ofertas:
            time.sleep(4)
            enviar_mensaje_telegram(oferta_key, oferta_info)
 
def enviar_mensaje_telegram(oferta_key, oferta_info):
    
    oferta = Oferta(

        titulo = oferta_info.get("titulo"),
        link_afiliado = oferta_info.get("link_afiliado"),
        precio_original= oferta_info.get("precio_original"),
        precio = oferta_info.get("precio"), 
        img = oferta_info.get("img"),
        oferta_id = oferta_info.get("oferta_id"),
        producto_id = oferta_info.get("producto_id"),
        categoria = oferta_info.get("categoria"),
        porcentaje = oferta_info.get("porcentaje")
        
    )

    foto_referencia = Imagenes.ik_subir_imagen(oferta)
    
    url_foto = foto_referencia.get("url")
    file_id = foto_referencia.get("fileId")
    chat_id = None

    chat_id, nombre = obtener_chatid_telegram(oferta.categoria) or (None, None)

    if oferta.porcentaje != 0:
        mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕ AHORRAS UN <b> {oferta.porcentaje}% </b>⭕\n\n📍 {oferta.titulo} \n\n <b>🔥{oferta.precio}€\n</b> <del>🚫{oferta.precio_original}€</del>\n\n \t\t\t\t🔰 <a href="{oferta.link_afiliado}">ENLACE DE COMPRA</a> \n\n {nombre}'
    else:
        mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕¡Nuevo Descuento Encontrado!⭕\n\n📍 {oferta.titulo} \n\n  \t🔰<a href="{oferta.link_afiliado}">ENLACE DE COMPRA</a>\n\n {nombre}'
    
    print(chat_id)

    if chat_id:
        id_mensaje = bot.send_message(chat_id,mensaje,parse_mode="html")

        oferta.id_mensaje = id_mensaje.message_id
        oferta.referencia_img = file_id
        oferta.oferta_key = oferta_key

        oferta.actualizar_estado(db)
    else:
        print('No se encontro Chat')


def actualizar_mensaje():

    ofertas = db.buscar_ofertas_publicadas()
    # Obtener la fecha actual del sistema
    fecha_actual = datetime.date.today()
    for key, oferta in ofertas:

        # Convertir la fecha en formato de cadena a tipo datetime
        fecha_cadena = oferta.get("fecha")
        # PRUEBA fecha_cadena = "2023-08-01"
        fecha = datetime.datetime.strptime(fecha_cadena, "%Y-%m-%d").date()

        # Restar dos días a la fecha actual
        fecha_dos_dias_antes = fecha_actual - datetime.timedelta(days=1)

        # Comprobar si la fecha es dos días más antigua
        if fecha < fecha_dos_dias_antes:
            print("La fecha", fecha_cadena, "es dos días más antigua que la fecha actual del sistema se Agota.")
            time.sleep(4)
            foto_referencia = Imagenes.ik_actualizar_imagen(oferta)
            url_foto = foto_referencia.get("url")
            id_chat,nombre = obtener_chatid_telegram(oferta.get("categoria"))
            if oferta.get("porcentaje") != 0:
                mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕ AHORRAS UN <b> {oferta.get("porcentaje")}% </b>⭕\n\n 📍 {oferta.get("titulo")}\n\n <b>🔥{oferta.get("precio")}€</b>\n 🚫<del>{oferta.get("precio_original")}€</del> \n\n \t🔰 <a href="{oferta.get("link_afiliado")}">❌ AGOTADO</a> \n\n {nombre}'
            
            else:
                mensaje = f'<a href="{url_foto}">&#8205</a>✨#Amazon✨\n\n ⭕¡Nuevo Descuento Encontrado!⭕\n\n📍 {oferta.get("titulo")} \n\n \t🔰<a href="{oferta.get("link_afiliado")}">❌ AGOTADO</a>\n\n {nombre}'
            try:
                db.actualizar_estado_agotado_oferta(oferta.get("categoria"), key)
                print(oferta.get("id_mensaje"))
                bot.edit_message_text(mensaje,id_chat,int(oferta.get("id_mensaje")),parse_mode="html")
            except telebot.apihelper.ApiTelegramException as e:
                
                print(f"Error al editar el mensaje de {key}:", e)

        else:
            print("La fecha", fecha_cadena, "no es dos días más antigua que la fecha actual del sistema.")



def obtener_chatid_telegram(categoria):
    if categoria == "libros":
        return CHAT_EBOOK, '@chollosebook'
    elif categoria == "videojuegos":
        return CHAT_JUEGOS, '@chollosjuego'
    elif categoria == "figuras":
        return CHAT_FIGURAS,'@chollosfiguras'
    elif categoria == "todo":
        return CHAT_TODOS,'@amazonoferta_es'
    elif categoria == "naturaleza-y-deportes-de-invierno":
        return CHAT_CAMPING,'@cholloscampings'
    elif categoria == "salud-y-cosmeticos":
        return CHAT_SALUD,'@chollossalud'
    
    # Agrega más condiciones para cada categoría que tengas


