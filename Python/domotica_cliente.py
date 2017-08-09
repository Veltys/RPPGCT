#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_cliente.py
# Description   : Parte cliente del sistema gestor de domótica
# Author        : Veltys
# Date          : 09-08-2017
# Version       : 1.0.1
# Usage         : python3 domotica_cliente.py [commands]
# Notes         : Parte cliente del sistema en el que se gestionarán pares de puertos GPIO


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema

try:
  from config import domotica_cliente_config as config                          # Configuración

except ImportError:
  print('Error: Archivo de configuración no encontrado', file = sys.stderr)
  sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas
# import comun                                                                    # Funciones comunes a varios sistemas
import os                                                                       # Funcionalidades varias del sistema operativo
import socket                                                                   # Tratamiento de sockets


class domotica_cliente(object):
    def __init__(self, config, argumentos):
        self._argumentos = argumentos
        self._config = config
        self._estado = 0
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def _comprobar_lista_GPIOs(self):
        try:
            self._lista_GPIOs

        except AttributeError:
            return False

        else:
            return True


    def __comando(self):
        if len(self._argumentos) == 1:
            comando = input('Introduzca un comando: ')
            comando = comando.lower()

        else:
            comando = self._argumentos[1]
            self._argumentos.pop(1)

        return comando


    def __conectar(self, comando):
        if self._estado == 0:
            print('Info: Conectando a ' + comando[9:])

            try:
                self._socket.connect((comando[9:], self._config.puerto))

            except TimeoutError:
                print('Error: Tiempo de espera agotado al conectar a ' + comando[9:], file = sys.stderr)

            except ConnectionRefusedError:
                print('Error: Imposible conectar a ' + comando[9:], file = sys.stderr)

            else:
                print('Ok: Conectado a ' + comando[9:])
                self._estado = 1

            return True

        else:
            print('Error: Imposible conectar a ' + comando[9:] + ', ya hay una conexión activa', file = sys.stderr)

            return False


    def __enviar_y_recibir(self, comando):
        self._socket.send(comando.encode('utf-8'))
        mensaje = self._socket.recv(1024)
        mensaje = mensaje.decode('utf-8')
        mensaje = mensaje.lower()

        return mensaje


    def __estado(self, comando):
        if self._estado >= 2:
            mensaje = self.__enviar_y_recibir(comando)

            if mensaje[0:4] == 'info' and (int(mensaje[6:]) == 0 or int(mensaje[6:]) == 1):
                return mensaje[6:]

            else:
                return -1

        else:
            return -1


    def __listar(self):
        if self._estado >= 1:
            self._lista_GPIOs = self.__enviar_y_recibir('listar')
            self._lista_GPIOs = self._lista_GPIOs[6:-1]
            self._lista_GPIOs = self._lista_GPIOs.split(' ')

            if self._comprobar_lista_GPIOs():
                self._estado = 2

                for i in range(len(self._lista_GPIOs)):
                    aux = self._lista_GPIOs[i]
                    self._lista_GPIOs[i] = list()
                    self._lista_GPIOs[i].append(aux)
                    self._lista_GPIOs[i].append(self.__estado('estado ' + aux))

            return True

        else:
            print('Error: Imposible solicitar una lista de puertos GPIO, no ' + self.estado(self._estado + 1), file = sys.stderr)

            return False


    def __mostrar_lista(self):
        if self._estado >= 2:
            print('Ok: Puertos GPIO que están disponibles:')

            for puerto, estado in self._lista_GPIOs:
                print("\t" + 'Puerto GPIO' + puerto + ' --> Estado: ' + ('activo' if estado == 1 else 'inactivo'), sep = '')

            return True

        else:
            print('Error: No hay ninguna lista de puertos GPIO cargada', file = sys.stderr)

            return False


    def __mostrar_estado(self, puerto, estado):
        if self._estado >= 2:
            if int(estado) == 0 or int(estado) == 1:
                print('Ok: Puerto GPIO' + puerto + ' --> Estado: ' + ('activo' if estado == 1 else 'inactivo'), sep = '')

                return True

            else:
                print('Error: El número de puerto GPIO no es válido', file = sys.stderr)

                return False

        else:
            print('Error: No hay ninguna lista de puertos GPIO cargada', file = sys.stderr)

            return False


    def __varios(self, comando):
        if self._estado >= 2:
            mensaje = self.__enviar_y_recibir(comando)

            if mensaje[0:2] == 'ok':
                print('Correcto: El servidor informa de que el comando "' + comando + '" ha sido ' + mensaje[4:], sep = '')

            elif mensaje[0:4] == 'info' and (int(mensaje[5:]) == 0 or int(mensaje[5:]) == 1):
                print('Correcto: El servidor informa de que el estado del puerto "GPIO' + comando[7:] + '" es ' + mensaje[5:], sep = '')

            else:
                print('Aviso: El servidor informa de que el comando "' + comando + '" es ' + mensaje[5:], sep = '')

        elif self._estado == 1:
            print('Aviso: El comando "' + comando + '" no ha sido ejecutado porque no' + self.estado(self._estado + 1), sep = '')

        else:
            print('Error: Imposible interaccionar con el puerto GPIO solicitado, no ' + self.estado(self._estado + 1), file = sys.stderr)


    def arranque(self):
        return 0                                                                # En este caso, no es necesario realizar operaciones de arranque


    def bucle(self):
        try:
            comando = self.__comando()

            while comando != 'salir':
                # conectar & listar & estado
                if comando != 'conectar' and comando[0:8] == 'conectar' and comando[8] == ' ' and comando[9:] != '':
                    if self.__conectar(comando):
                        if self.__listar():
                            self.__mostrar_lista()


                # listar
                elif comando == 'listar':
                    if self.__listar():
                        self.__mostrar_lista()

                # conmutar, pulsar, encender, apagar
                elif (comando != 'conmutar' and comando[0:8] == 'conmutar' and comando[8] == ' ' and comando[9:] != '') \
                  or (comando != 'pulsar'   and comando[0:6] == 'pulsar'   and comando[6] == ' ' and comando[7:] != '') \
                  or (comando != 'encender' and comando[0:8] == 'encender' and comando[8] == ' ' and comando[9:] != '') \
                  or (comando != 'apagar'   and comando[0:6] == 'apagar'   and comando[6] == ' ' and comando[7:] != '') \
                  :
                    self.__varios(comando)

                # estado
                elif comando != 'estado' and comando[0:6] == 'estado' and comando[6] == ' ' and comando[7:] != '':
                    self.__mostrar_estado(comando[7:], self.__estado(comando))


                # conmutar, pulsar, encender, apagar o estado pero sin parámetros
                elif comando == 'conectar' \
                  or comando == 'conmutar' \
                  or comando == 'pulsar'   \
                  or comando == 'encender' \
                  or comando == 'apagar'   \
                  or comando == 'estado'   \
                  :
                    print('Error: El comando "' + comando + '" requiere uno o más parámetros. Por favor, inténtelo de nuevo.', file = sys.stderr)

                # desconectar
                elif comando == 'desconectar':
                    self.cerrar()

                else:
                    print('Error: El comando "' + comando + '" no ha sido reconocido. Por favor, inténtelo de nuevo.', file = sys.stderr)

                print()                                                         # Llamar a print() sin argumentos introduce una nueva línea
                comando = self.__comando()

            # salir                                                             # La salida propiamente dicha será ejecutada en la siguiente vuelta del bucle
            if comando == 'salir':
                self.cerrar()

        except KeyboardInterrupt:
            self.cerrar()
            return


    def cerrar(self):
        if self._estado >= 1:
            self._socket.sendall('desconectar'.encode('utf-8'))
            self._socket.close()
            self._estado = 0


    def estado(self, estado = False):
        if estado == False:
            estado = self._estado

        if estado == 0:
            return 'no hay una conexión activa'

        elif estado == 1:
            return 'hay una conexión activa'

        elif estado == 2:
            return 'hay una lista de puertos GPIO cargada'

        else:
            return 'el estado es desconocido'


    def __del__(self):
        pass


def main(argv = sys.argv):
    app = domotica_cliente(config, sys.argv)
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
