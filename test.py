import Chollo
import telegram_chat


import time
import random


def ejecutable():
    Chollo.scrape()
    print('--------- SCRAPE TERMINADO -------------')
    telegram_chat.main()

delay_min = 1500
delay_max = 3600


while True:
    
    retardo = random.uniform(delay_min, delay_max)
    # Verificar si hay tareas programadas y ejecutarlas
    ejecutable()
    print("/////////////////////////////////////////////////////////////////////////////////////////////")
    time.sleep(retardo)

    # Esperar un segundo antes de verificar nuevamente
    
