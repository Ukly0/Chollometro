import Scrape
import Mensajes
import random
import time

while True:

    aleatorio_en_segundos = random.randint(3600, 7200)
    
    Scrape.scrape()
    Mensajes.enviar_mensaje()
    #Mensajes.actualizar_mensaje()
    print(f'ESPERANDO PROXIMA VUELTA EN {aleatorio_en_segundos} segundos' )
    time.sleep(aleatorio_en_segundos)