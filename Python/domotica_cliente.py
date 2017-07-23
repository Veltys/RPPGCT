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
  print('Error: Archivo de configuración no encontrado', file = sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import socket                                                                   # Tratamiento de sockets


class domotica_cliente(comun.app):
    def __init__(self, config, nombre = False):
        super().__init__(config, nombre)

        self._estado = 0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def bucle(self):
        try:
            comando = input('Introduzca un comando: ')
            comando = comando.lower()

            while comando != 'salir':
                # conectar
                if comando != 'conectar' and comando[0:8] == 'conectar' and comando[8] == ' ' and comando[9:] != '':
                    if self._estado == 0:
                        print('Conectando a ' + comando[9:])

                        try:
                            self._socket.connect((comando[9:], self._config.puerto))

                        except TimeoutError:
                            print('Error: Tiempo de espera agotado al conectar a ' + comando[9:], file = sys.stderr)

                        except ConnectionRefusedError:
                            print('Error: Imposible conectar a ' + comando[9:], file = sys.stderr)

                        else:
                            print('Conectado a ' + comando[9:])
                            self._estado = 1

                    else:
                        print('Error: Imposible conectar a ' + comando[9:] + ', ya hay una conexión activa', file = sys.stderr)

                # listar
                elif comando == 'listar':
                    if self._estado >= 1:
                        self._socket.send(comando.encode('utf-8'))
                        self._lista_GPIOs = self._socket.recv(1024)
                        self._lista_GPIOs = self._lista_GPIOs.decode('utf-8')

                        self._lista_GPIOs = self._lista_GPIOs.split(' ')

                        if self.mostrar_lista_GPIOs():
                            self._estado = 2

                    else:
                        print('Error: Imposible solicitar una lista de puertos GPIO, no ' + self.estado(self._estado + 1), file = sys.stderr)

                # conmutar, pulsar, encender o apagar
                elif (comando != 'conmutar' and comando[0:8] == 'conmutar' and comando[8] == ' ' and comando[9:] != '') \
                  or (comando != 'pulsar'   and comando[0:6] == 'pulsar'   and comando[6] == ' ' and comando[7:] != '') \
                  or (comando != 'encender' and comando[0:8] == 'encender' and comando[8] == ' ' and comando[9:] != '') \
                  or (comando != 'apagar'   and comando[0:6] == 'apagar'   and comando[6] == ' ' and comando[7:] != ''):
                    if self._estado >= 2:
                        self._socket.send(comando.encode('utf-8'))
                        mensaje = self._socket.recv(1024)
                        mensaje = mensaje.decode('utf-8')
                        mensaje = mensaje.lower()

                        if mensaje[0:2] == 'ok':
                            print('Correcto: El servidor informa de que el comando "' + comando + '" es ' + mensaje[4:], sep = '')

                        else:
                            print('Aviso: El servidor informa de que el comando "' + comando + '" es ' + mensaje[5:], sep = '')

                    else:
                        print('Error: Imposible interaccionar con el puerto GPIO solicitado, no ' + self.estado(self._estado + 1), file = sys.stderr)

                elif comando == 'conectar' or comando == 'conmutar' or comando == 'pulsar' or comando == 'encender' or comando == 'apagar':
                    print('Error: El comando "' + comando + '" requiere uno o más parámetros. Por favor, inténtelo de nuevo.', file = sys.stderr)

                else:
                    print('Error: El comando "' + comando + '" no ha sido reconocido. Por favor, inténtelo de nuevo.', file = sys.stderr)

                comando = input('Introduzca un comando: ')

            # salir                                                             # La salida propiamente dicha será ejecutada en la siguiente vuelta del bucle
            if comando == 'salir' and self._estado >= 2:
                self._socket.sendall(comando.encode('utf-8'))

        except KeyboardInterrupt:
            self.cerrar()
            return


    def cerrar(self):
        if self._estado >= 2:
            self._socket.sendall(comando.encode('utf-8'))

        super().cerrar()

    def estado(self, estado = False):
        if estado == False:
            estado = self._estado

        if estado == 0:
            return 'no hay una conexión activa'

        elif estado == 1:
            return 'hay una conexión activa'

        elif estado == 2:
            return 'hay una lista de puertos GPIO cargada'


    def mostrar_lista_GPIOs(self):
        try:
            self._lista_GPIOs

        except AttributeError:
            print('Error: No hay ninguna lista de puertos GPIO cargada', file = sys.stderr)

            return False

        else:
            print('Puertos GPIO que están activos:')

            for puerto in self._lista_GPIOs:
                print("\t" + puerto, sep = '')

            return True


    def __del__(self):
        super().__del__()


def main(argv = sys.argv):
     app = domotica_cliente(config)
     app.arranque()


if __name__ == '__main__':
    main(sys.argv)
