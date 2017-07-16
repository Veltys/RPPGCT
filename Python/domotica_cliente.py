#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_cliente.py
# Description   : Parte cliente del sistema gestor de domótica
# Author        : Veltys
# Date          : 15-07-2017
# Version       : 0.1.0
# Usage         : python3 domotica_cliente.py
# Notes         : Parte cliente del sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Pendiente (TODO): Por ahora solamente responde a un pulsador local, queda pendiente la implementación remota (sockets)
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import domotica_cliente_config as config                          # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file=sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
# import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import socket                                                                   # Tratamiento de sockets


class domotica_cliente(comun.app):
    def __init__(self, config, nombre):
        self._socket = socket.socket()

        super().__init__(config, nombre)

    def bucle(self):
        try:
            while True:
                comando = input('Introduzca un comando: ')

                if comando[0:8].lower() == 'conectar' and comando[8] == ' ' and comando[9:] != '':
                    print('Conectando a ' + comando[9:])

                    try:
                        self._socket.connect((comando[9:], 4710))               # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
                                                                                # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85

                    except TimeoutError:
                        print('Error: Tiempo de espera agotado al conectar a ' + comando[9:], file=sys.stderr)

                elif comando[0:5].lower() == 'salir':
                    sys.exit(0)

                else:
                    print('Error: El comando "' + comando + '" no ha sido reconocido. Por favor, inténtelo de nuevo.', file=sys.stderr)
                    

                sleep(self._config.PAUSA)

        except KeyboardInterrupt:
            sys.exit(0)

    def __del__(self):
        super().__del__()


def main(argv = sys.argv):
     app = domotica_cliente(config, os.path.basename(sys.argv[0]))
     app.arranque()


if __name__ == '__main__':
    main(sys.argv)
