#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica.py
# Description   : Sistema gestor de domótica
# Author        : Veltys
# Date          : 06-07-2017
# Version       : 1.0.0
# Usage         : python3 domotica.py
# Notes         : Sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import domotica_config as config                                  # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
# import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
# import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


from multiprocessing import Process
from random import random


# class domotica(comun.app):
#     def __init__(self, config):
#         super().__init__(config)
# 
#     def bucle():
#         try:
#             i = 1
# 
#             while True:
#                 print('Esperando un evento en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep='')
#                 GPIO.wait_for_edge(GPIO_BOTON, GPIO.RISING)
#                 print('Se ha detectado un evento de activación en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep = '')
#                 GPIO.wait_for_edge(GPIO_BOTON, GPIO.FALLING)
#                 print('Se ha detectado un evento de desactivación en el PIN GPIO', GPIO_BOTON, "\r\nID del evento: ", i, sep='')
#                 i = i + 1
# 
#         except KeyboardInterrupt:
#             self.cerrar()


class tarea:
    
    def __init__(self, cid):
        self.__cid=cid
        print("HIJO {0} - Nace".format(self.__cid))
    
    def __del__(self):
        print("HIJO {0} - Muere".format(self.__cid))
    
    def run(self):
        
        # Generamos un tiempo de espera aleatorio
        s=1+int(10*random())
        
        print("HIJO {0} - Inicio (Durmiendo {1} segundos)".format(self.__cid,s))
        sleep(s)
        print("HIJO {0} - Fin".format(self.__cid))
 
 
def main(argv = sys.argv):
#     app = domotica(config)
#     app.arranque(os.path.basename(argv[0]))

    # Creamos la piscina (Pool)
    piscina = []
    for i in range(1,5):
#    for i in range(int(len(config.GPIOS) / 2)):
        print("PADRE: creando HIJO {0}".format(i))
        piscina.append(Process(name="Proceso {0}".format(i), target=tarea(i).run))
     
    # Arrancamos a todos los hijos
    print("PADRE: arrancando hijos")
    for proceso in piscina:
        proceso.start()
     
    print("PADRE: esperando a que los procesos hijos hagan su trabajo")
    # Mientras la piscina tenga procesos
    while piscina:
        # Para cada proceso de la piscina
        for proceso in piscina:
            # Revisamos si el proceso ha muerto
            if not proceso.is_alive():
                # Recuperamos el proceso y lo sacamos de la piscina
                proceso.join()
                piscina.remove(proceso)
                del(proceso)
        
        # Para no saturar, dormimos al padre durante 1 segundo
        print("PADRE: esperando a que los procesos hijos hagan su trabajo")
        sleep(1)
 
    print("PADRE: todos los hijos han terminado, cierro")


if __name__ == '__main__':
    main(sys.argv)
