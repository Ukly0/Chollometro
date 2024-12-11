import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image  
import os
# Cargar la imagen
imagen = cv2.imread(os.path.join("Ofertas", "1082872.jpg"))

FUENTE_PRECIO = os.path.join("Fuente", "Poppins-ExtraBold.ttf")
FUENTE_PRECIO_SIZE = 160 # Reemplaza con la ruta de tu archivo TTF

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
    cv2.imshow('Imagen con Rectángulo Negro Transparente y Texto', imagen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()