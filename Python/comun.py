#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : comun.py
# Description   : Módulo de funciones comunes a varios sistemas
# Author        : Veltys
# Date          : 06-03-2018
# Version       : 0.3.1
# Usage         : import comun | from comun import <clase>
# Notes         : ...


DEBUG = False


from abc import ABCMeta, abstractmethod                                         # Clases abstractas
from pid import bloqueo                                                         # Módulo propio para bloquear la ejecución de más de una instancia
from time import sleep                                                          # Para hacer pausas
import errno                                                                    # Códigos de error
import os                                                                       # Funcionalidades varias del sistema operativo
import signal                                                                   # Manejo de señales
import sys                                                                      # Funcionalidades varias del sistema
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO
import socket                                                                   # Tratamiento de sockets


class app(object):
    # Clase abstracta que contiene todos los métodos comunes para una app de este sistema

    __metaclass__       = ABCMeta
    _config             = []
    _bloqueo            = False
    _estado             = 0
    _modo_apagado       = False
    _socket             = False
    _VERSION_PROTOCOLO  = 1.1


    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
            - Asigna señales a sus correspondientes funciones
        '''

        self._config = config
        self._bloqueo = bloqueo(nombre) if not(nombre == False) else False      # No siempre va a ser necesario realizar un bloqueo

        self.asignar_senyales()


    def _conectar(self, comando, salida = True):
        ''' Realiza una conexión contra un servidor dado en el parámetro "comando"
            - Comprueba el estado de la conexión
                - Si es == 0 (no hay una conexión activa), intenta conectar
                    - Si no puede conectar por algún motivo, informa del error (si procede) y retorna "False"
                    - Si sí, conecta, informa (si procede) y retorna la versión del proteocolo empleada
                - Si no, informa del error (si procede) y retorna "False"
        '''

        if self._estado == 0:
            if salida:
                print('Info: Conectando a ' + comando[9:])

            try:
                self._socket.connect((comando[9:], self._config.puerto))

            except TimeoutError:
                print('Error: Tiempo de espera agotado al conectar a ' + comando[9:], file = sys.stderr)

                return False

            except ConnectionRefusedError:
                print('Error: Imposible conectar a ' + comando[9:], file = sys.stderr)

                return False

            except AttributeError:
                return False

            else:
                if salida:
                    print('Ok: Conectado a ' + comando[9:])

                self._estado = 1

                mensaje = self._enviar_y_recibir('hola ' + str(self._VERSION_PROTOCOLO))

                if mensaje == False:                                            # Si hay algún fallo al conectar con el servidor, simplemente informaremos de este fallo
                    return False

                elif(mensaje[:2] == 'ok'):                                      # Si el servidor nos da un ok, significa que la versión del protocolo que tenemos es la adecuada
                    return True

                elif(mensaje[:4] == 'info'):                                    # Si el servidor nos da un info, significa que usaremos una versión anterior
                    self._VERSION_PROTOCOLO = float(mensaje[5:])

                    return True

                else:                                                           # Si nos da un err u otra cosa, el protocolo es incompatible y desconectaremos
                    self._desconectar()

                    return False

        else:
            print('Error: Imposible conectar a ' + comando[9:] + ', ya hay una conexión activa', file = sys.stderr)

            return False


    def _desconectar(self):
        ''' Desconecta, si se está conectado, una conexión existente contra un servidor
            - Comprueba el estado de la conexión
            - Si el estado es >= 1 (hay una conexión activa), la desconecta
            - Si no, no hace nada
        '''

        if self._estado >= 1:
            self._socket.sendall('desconectar'.encode('utf-8'))
            self._socket.close()
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._estado = 0


    def _enviar_y_recibir(self, comando, normalizar = True):
        ''' Envía un comando dado en el parámetro "comando" y recibe la respuesta correspondiente
            - Comprueba si existe el socket e intenta utilizarlo
                - Si no, retorna "False"
                - Si sí, recibe el mensaje y lo retorna
        '''

        if self._socket != False:
            self._socket.send(comando.encode('utf-8'))

            mensaje = self._socket.recv(1024)
            mensaje = mensaje.decode('utf-8')

            if normalizar:
                mensaje = mensaje.lower()

            return mensaje

        else:
            return False


    def _sig_apagado(self, signum, frame):
        # Funcion "wrapper" para el procesamiento de la señal de apagado

        self.apagado()


    def _sig_cerrar(self, signum, frame):
        # Funcion "wrapper" para el procesamiento de la señal de cierre

        self.cerrar()
        os._exit(0)


    def _sig_test(self, signum, frame):
        # Funcion "wrapper" para el procesamiento de la señal de pruebas

        self.test()


    def apagado(self):
        ''' Activador / desactivador del "modo apagado":
            - Conmuta el "modo apagado"
            - "Apaga" todos los puertos GPIO
        '''

        self._modo_apagado = not(self._modo_apagado)

        for gpio, _, activacion, _ in self._config.GPIOS:
            GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)


    def arranque(self):
        ''' Lleva a cabo las tareas necesarias para el "arranque" de la app:
            - Comprueba si hay otra instancia en ejecución
                - Si no, establece un bloqueo para evitar otras ejecuciones
                - Si sí, sale
            - Configura los puertos GPIO
        '''

        if self._bloqueo == False or self._bloqueo.comprobar():
            if self._bloqueo == False or self._bloqueo.bloquear():
                try:
                    self._config.GPIOS

                except AttributeError:
                    pass

                else:
                    GPIO.setmode(GPIO.BCM)                                      # Establecemos el sistema de numeración BCM

                    GPIO.setwarnings(DEBUG)                                     # De esta forma alertará de los problemas sólo cuando se esté depurando

                    for i in range(len(self._config.GPIOS)):                    # Se configuran los pines GPIO como salida o entrada en función de lo leído en la configuración
                        if DEBUG:
                            print('Proceso  #', os.getpid(), "\tPreparando el puerto GPIO", self._config.GPIOS[i][0], sep = '')

                        if self._config.GPIOS[i][1]:
                            if DEBUG:
                                print('Proceso  #', os.getpid(), "\tConfigurando el puerto GPIO", self._config.GPIOS[i][0], ' como salida', sep = '')

                            GPIO.setup(self._config.GPIOS[i][0], GPIO.OUT, initial = GPIO.LOW if self._config.GPIOS[i][2] else GPIO.HIGH)

                        else:
                            if DEBUG:
                                print('Proceso  #', os.getpid(), "\tConfigurando el puerto GPIO", self._config.GPIOS[i][0], 'como entrada', sep = '')

                            GPIO.setup(self._config.GPIOS[i][0], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
                            self._config.GPIOS[i] = list(self._config.GPIOS[i]) # En el caso de tener un pin GPIO de entrada, se necesitará transformar en lista la tupla, ya que es posible que haga falta modificar su contenido

                return 0

            else:
                print('Error: No se puede bloquear ' + self._bloqueo.nombre(), file = sys.stderr)
                return errno.EACCES

        else:
            print('Error: Ya se ha iniciado una instancia de ' + self._bloqueo.nombre(), file = sys.stderr)
            return errno.EEXIST


    def asignar_senyales(self):
        ''' Asigna señales a sus correspondientes funciones:
                - Comprueba si existe la variable correspondiente
                    - Si no, no hace nada
                    - Si sí, asigna la señal especificada con la función correspondiente
        '''

        try:
            self._config.senyales

        except AttributeError:
            pass

        else:
            for senyal, funcion in self._config.senyales.items():
                signal.signal(eval('signal.' + senyal), eval('self._' + funcion))


    @abstractmethod
    def bucle(self):
        # Función abstracta que será especificada en el sistema que la incluya

        pass


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema:
            - "Limpia" los puertos GPIO que hayan podido usarse
            - Desbloquea la posible ejecución de otra futura instancia del mismo sistema
        '''

        self._desconectar()

        try:
            self._config.GPIOS

        except AttributeError:
            pass

        else:
            GPIO.cleanup()                                                          # Devolvemos los pines a su estado inicial

        if not(self._bloqueo == False):
            self._bloqueo.desbloquear()


    def estado(self, estado = False):
        ''' Función "sobrecargada" gracias al parámetro "estado"
            - Para "estado" == "False"
                - Actúa como pseudo-observador de la variable "_estado" de la clase
            - Para "estado" != "False"
                - Actúa como modificador de la variable "_estado" de la clase
        '''

        if estado == False:
            if self._estado == 0:
                return 'no hay una conexión activa'

            elif self._estado == 1:
                return 'hay una conexión activa'

            elif self._estado == 2:
                return 'hay una lista de puertos GPIO cargada'

            else:
                return 'el estado es desconocido'

        else:
            self._estado = estado


    def test(self):
        # Ejecuta el modo de pruebas

        try:
            self._config.GPIOS

        except AttributeError:
            pass

        else:
            for gpio, _, activacion, _ in self._config.GPIOS:
                GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)

            sleep(self._config.PAUSA)


    def __del__(self):
        # Destructor de la clase: Ya que su ejecución no está asegurada, no hace nada

        pass
