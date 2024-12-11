# Chollometro Scraper & Telegram Poster

## Descripción
Esta aplicación realiza web scraping de la plataforma Chollometro para encontrar ofertas de Amazon, modifica los enlaces de los productos encontrados para incluir enlaces de afiliados y publica los chollos en un canal de Telegram.

---



## Características
- **Web Scraping:** Obtiene información de ofertas populares de Chollometro.
- **Filtrado de Productos:** Solo selecciona ofertas de Amazon con una temperatura mínima.
- **Generación de Enlaces de Afiliados:** Crea enlaces de afiliados para cada oferta.
- **Gestión de Imágenes:** Descarga imágenes de productos.
- **Historial de Ofertas:** Registra los chollos nuevos en un archivo Excel.

---

## Categorías del Proyecto
- **Scraper de Ofertas:** Extrae datos de productos de Chollometro.
- **Gestión de Imágenes:** Descarga y almacena imágenes de productos.
- **Generador de Enlaces de Afiliados:** Crea enlaces personalizados para Amazon.
- **Gestión de Historial:** Registra y compara ofertas anteriores.
- **Publicador en Telegram:** Publica ofertas en un canal de Telegram configurado.

| Categoría Juegos               | Categoría Salud               |
|-----------------------|-------------------------|
| ![Texto 1](chollosjuego.jpg) | ![Texto 2](chollossalud.jpg) |
| Categoría Libros             | Categoría Camping            |
| ![Texto 3](chollosebook.jpg) | ![Texto 4](cholloscampings.jpg) |

---

## Requisitos

### Bibliotecas de Python
- `requests` - Para realizar solicitudes HTTP.
- `openpyxl` - Para manejar archivos Excel.
- `selenium` - Para la automatización de navegación web.
- `bs4 (BeautifulSoup)` - Para analizar HTML.

### Software
- **Chromedriver:** Asegúrate de tener `chromedriver` instalado y configurado.

---

## Instalación
1. **Clonar el Repositorio:**
   ```bash
   git clone https://github.com/tu-repositorio/chollometro-scraper.git
   cd chollometro-scraper
   ```

2. **Crear un Entorno Virtual y Activarlo:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. **Instalar Dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Chromedriver:**
   - Descarga e instala [Chromedriver](https://chromedriver.chromium.org/downloads).
   - Configura la ruta en el archivo principal.

---

## Uso

1. **Ejecutar el Script:**
   ```bash
   python main.py
   ```

2. **Personalización:**
   - Modifica la variable `delay_min` y `delay_max` para ajustar los tiempos de espera.
   - Configura el canal de Telegram para publicaciones automáticas.

---

## Estructura del Proyecto
```
chollometro-scraper/
├── main.py              # Archivo principal
├── Imagenes/            # Carpeta para imágenes descargadas
├── historico_chollos.xlsx # Archivo de historial de chollos
├── nuevos_chollos.xlsx  # Archivo de chollos nuevos
├── requirements.txt     # Dependencias del proyecto
└── README.md            # Documento de referencia
```

---

## Personalización
- **Temperatura Mínima:** Cambia el valor en el script para filtrar solo ofertas relevantes.
- **Tienda:** Actualmente solo filtra ofertas de Amazon.
- **Enlace de Afiliado:** Configura tu código de afiliado en la variable `linkAfiliado`.

---

## Contribuciones
¡Las contribuciones son bienvenidas! Realiza un fork del proyecto y envía tus cambios mediante un pull request.

**¿Tienes alguna idea loca o una mejora inesperada?** 🎯

¡Anímate y haz un pull request! No importa si es grande o pequeño, toda ayuda es bienvenida. 💪

---

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.

---

## Advertencia
Este proyecto es solo con fines educativos. El uso de bots y scrapers puede violar los términos de servicio de algunos sitios web. Utilízalo bajo tu propia responsabilidad.

---

¡Gracias por usar Chollometro Scraper & Telegram Poster! 🎉

