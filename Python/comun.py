#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : comun.py
# Description   : Módulo de funciones comunes a varios sistemas
# Author        : Veltys
# Date          : 13-07-2018
# Version       : 0.5.0
# Usage         : import comun | from comun import <clase>
# Notes         : ...


DEBUG           = False


import errno                                                                            # Códigos de error
import os                                                                               # Funcionalidades varias del sistema operativo
import signal                                                                           # Manejo de señales
import socket                                                                           # Tratamiento de sockets
import sys                                                                              # Funcionalidades varias del sistema

import RPi.GPIO as GPIO                                                                 # Acceso a los pines GPIO

from abc import ABCMeta, abstractmethod                                                 # Clases abstractas
from time import sleep                                                                  # Para hacer pausas

from pid import bloqueo                                                                 # Módulo propio para bloquear la ejecución de más de una instancia


class estados_conexion():
    DESCONECTADO    = 0
    CONECTADO       = 1
    LISTA_CARGADA   = 2
    LISTA_EXTENDIDA = 3


class app(object):
    ''' Clase abstracta que contiene todos los métodos comunes para una app de este sistema
    '''

    __metaclass__       = ABCMeta

    _VERSION_PROTOCOLO  = 1.1


    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
            - Asigna señales a sus correspondientes funciones
        '''

        self._bloqueo           = bloqueo(nombre) if not(nombre == False) else False    # No siempre va a ser necesario realizar un bloqueo
        self._config            = config
        self._estado_conexion   = estados_conexion.DESCONECTADO
        self._modo_apagado      = False
        self._socket            = False

        self.asignar_senyales()


    def _conectar(self, salida = True):
        ''' Realiza una conexión contra el servidor local
            - Comprueba el estado de la conexión
                - Si es == 0 (no hay una conexión activa), intenta conectar
                    - Si no puede conectar por algún motivo, informa del error (si procede) y retorna "False"
                    - Si sí, conecta, informa (si procede) y retorna la versión del proteocolo empleada
                - Si no, informa del error (si procede) y retorna "False"
        '''

        if self._estado_conexion == estados_conexion.DESCONECTADO:
            if salida:
                print('Info: Conectando al servidor...')

            try:
                self._socket.connect(('localhost', self._config.puerto))

            except TimeoutError:
                print('Error: Tiempo de espera agotado al conectar al servidor', file = sys.stderr)

                return False

            except ConnectionRefusedError:
                print('Error: Imposible conectar al servidor', file = sys.stderr)

                return False

            except AttributeError:
                return False

            else:
                if salida:
                    print('Ok: Conectado al servidor')

                self._estado_conexion = estados_conexion.CONECTADO

                mensaje = self._enviar_y_recibir('hola ' + str(self._VERSION_PROTOCOLO))

                if mensaje == False:                                                    # Si hay algún fallo al conectar con el servidor
                    return False                                                        #     Se informa del fallo

                elif(mensaje[:2] == 'ok'):                                              # Si el servidor devuelve un "ok" (significa que la versión del protocolo del servidor es la misma)
                    return True                                                         #     Se informa del éxito

                elif(mensaje[:4] == 'info'):                                            # Si el servidor devuelve un "info" (significa que el servidor usa una versión distinta)
                    self._VERSION_PROTOCOLO = float(mensaje[5:])                        #     Se informa del éxito

                    return True

                else:                                                                   # Si el servidor devuelve otra cosa (el protocolo es incompatible, ha sucedido algún problema, el servidor no responde, etc.)
                    self._desconectar()                                                 #     Se desconecta

                    return False                                                        #     Se informa del fallo

        else:
            print('Error: Imposible conectar al servidor, ya hay una conexión activa', file = sys.stderr)

            return False


    def _desconectar(self):
        ''' Desconecta, si se está conectado, una conexión existente contra un servidor
            - Comprueba el estado de la conexión
            - Si el estado es >= 1 (hay una conexión activa), la desconecta
            - Si no, no hace nada
        '''

        if self._estado_conexion >= estados_conexion.CONECTADO:
            self._socket.sendall('desconectar'.encode('utf-8'))
            self._socket.close()
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._estado_conexion = estados_conexion.DESCONECTADO


    def _enviar_y_recibir(self, comando, normalizar = True):
        ''' Envía un comando dado en el parámetro "comando", previamente normalizado a petición y recibe la respuesta correspondiente
            - Comprueba si existe el socket e intenta utilizarlo
                - Si no, retorna "False"
                - Si sí, recibe el mensaje y lo retorna
        '''

        if self._socket != False:
            try:                                                                        # Bloque try
                self._socket.send(comando.encode('utf-8'))                              #     Se manda el mensaje

            except BrokenPipeError:                                                     # Error de tubería rota
                comando = 'desconectar'                                                 #     Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

            except ConnectionResetError:                                                # Error de conexión reiniciada
                comando = 'desconectar'                                                 #     Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

            except OSError:                                                             # Error del sistema operativo
                comando = 'desconectar'                                                 #     Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

            else:                                                                       # Si todo ha ido bien (nótese la duplicidad de código; ¡gracias, Python, por no implementar la estructura do - while!)
                try:                                                                    #     Bloque try
                    mensaje = self._socket.recv(1024)                                   #         Ante un evento, se recibe el contenido

                except ConnectionResetError:                                            #     Error de conexión reiniciada
                    mensaje = 'desconectar'                                             #         Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

                else:                                                                   #     Si todo ha ido bien
                    mensaje = mensaje.decode('utf_8')                                   #         Se decodifica el mensaje recibido
                    mensaje = mensaje.lower()                                           #         Y se normaliza

            if normalizar:
                mensaje = mensaje.lower()

            return mensaje

        else:
            return False


    def _sig_apagado(self, signum, frame):
        ''' Funcion "wrapper" para el procesamiento de la señal de apagado
        '''

        self.apagado()


    def _sig_cerrar(self, signum, frame):
        ''' Funcion "wrapper" para el procesamiento de la señal de cierre
        '''

        self.cerrar()
        os._exit(0)


    def _sig_test(self, signum, frame):
        ''' Funcion "wrapper" para el procesamiento de la señal de pruebas
        '''

        self.test()


    def apagado(self):
        ''' Activador / desactivador del "modo apagado":
            - Conmuta el "modo apagado"
            - "Apaga" todos los puertos GPIO
        '''

        self._modo_apagado = not(self._modo_apagado)                                    # Se comuta el modo apagado

        for gpio, tipo, acceso, activacion, _ in self._config.GPIOS:                    # Se recorre la lista de puertos GPIO
            if tipo == self._config.LED:                                                #     Si se está ante un led
                GPIO.output(gpio, GPIO.LOW if activacion else GPIO.HIGH)                #         Se "apaga" de modo simple

            elif tipo == self._config.LED_PWM:                                          #     Si se está ante un led controlado por PWM
                acceso.ChangeDutyCycle(0)                                               #         Se "apaga" de modo ciclo de trabajo


    def arranque(self):
        ''' Lleva a cabo las tareas necesarias para el "arranque" de la aplicación:
            - Comprueba si hay otra instancia en ejecución
                - Si no, establece un bloqueo para evitar otras ejecuciones
                - Si sí, sale
            - Configura los puertos GPIO
        '''

        if self._bloqueo == False or not(self._bloqueo.comprobar()):
            if self._bloqueo == False or self._bloqueo.bloquear():
                try:
                    self._config.GPIOS

                except AttributeError:
                    pass

                else:
                    GPIO.setmode(GPIO.BCM)                                              # Establecemos el sistema de numeración BCM

                    GPIO.setwarnings(DEBUG)                                             # De esta forma alertará de los problemas sólo cuando se esté depurando

                    for i, puerto in enumerate(self._config.GPIOS):                     # Se configuran los pines GPIO como salida o entrada en función de lo leído en la configuración
                        puerto = list(puerto)                                           #     Se necesita transformar en lista la tupla, ya que es posible que haga falta modificar su contenido

                        if DEBUG:
                            print('Proceso  #', os.getpid(), "\tPreparando el puerto GPIO", puerto[0], sep = '')

                        if puerto[1] < self._config.BOTON:
                            if DEBUG:
                                print('Proceso  #', os.getpid(), "\tConfigurando el puerto GPIO", puerto[0], ' como salida', sep = '')

                            GPIO.setup(puerto[0], GPIO.OUT, initial = GPIO.LOW if puerto[2] else GPIO.HIGH)

                            if puerto[1] == self._config.LED_PWM:
                                puerto[2] = GPIO.PWM(puerto[0], self._config.FRECUENCIA)

                        else:
                            if DEBUG:
                                print('Proceso  #', os.getpid(), "\tConfigurando el puerto GPIO", self._config.GPIOS[i][0], 'como entrada', sep = '')

                            GPIO.setup(self._config.GPIOS[i][0], GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

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


    @abstractmethod                                                                     # Método abstracto
    def bucle(self):
        ''' Función abstracta que será especificada en el sistema que la incluya
        '''

        pass


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema:
            - "Limpia" los puertos GPIO que hayan podido usarse
            - Desbloquea la posible ejecución de otra futura instancia del mismo sistema
        '''

        self._desconectar()

        try:                                                                            # Bloque try
            self._config.GPIOS                                                          #     Se comprueba la existencia de puertos GPIO

        except AttributeError:                                                          # Si no los hay
            pass                                                                        #     Sin problema

        else:                                                                           # Si sí los hay
            for _, tipo, acceso, _, _ in self._config.GPIOS:                            #     Se recorren los pines GPIO
                if tipo == self._config.LED_PWM:                                        #         Si el pin es un led controlado por PWM
                    acceso.stop()                                                       #             Se le ordena parar

            GPIO.cleanup()                                                              #     Se liberan los pines GPIO

        if not(self._bloqueo == False):                                                 # Si hay un boqueo
            self._bloqueo.desbloquear()                                                 #     Se desbloquea

        # TODO: PID


    def estado_conexion(self, estado = False):
        ''' Método "sobrecargado" gracias al parámetro "estado"
            - Para "estado" == "False"
                - Actúa como observador de la variable "_estado_conexion" de la clase
            - Para "estado" != "False"
                - Actúa como modificador de la variable "_estado_conexion" de la clase
        '''

        if estado == False:
            return self._estado_conexion

        else:
            self._estado_conexion = estado


    @staticmethod                                                                       # Método estático
    def estado_conexion_lenguaje_natural(estado):
        ''' Observador en lenguaje natural de un estado de conexión dado
        '''

        if estado == 0:
            return 'no hay una conexión activa'

        elif estado == 1:
            return 'hay una conexión activa'

        elif estado == 2:
            return 'hay una lista de puertos GPIO cargada'

        elif estado == 3:
            return 'hay una lista extendida de puertos GPIO cargada'

        else:
            return 'el estado es desconocido'


    def test(self):
        ''' Ejecuta el modo de pruebas
        '''

        if DEBUG:
            print('Entrando en modo de pruebas')

        try:                                                                            # Bloque try
            self._config.GPIOS                                                          #     Se comprueba la existencia de puertos GPIO

        except AttributeError:                                                          # Si no los hay
            pass                                                                        #     Sin problema

        else:                                                                           # Si sí los hay
            if DEBUG:
                print('Encendiendo leds')

            for gpio, tipo, acceso, activacion, _ in self._config.GPIOS:                #     Se recorre la lista de puertos GPIO
                if tipo == self._config.RELE or tipo == self._config.LED:               #         Si se está ante un relé o un led normal
                    GPIO.output(gpio, GPIO.HIGH if activacion else GPIO.LOW)            #             Se "enciende" de modo normal

                elif tipo == self._config.LED_PWM:                                      #         Si se está ante un led controlado por PWM
                    acceso.ChangeDutyCycle(100)                                         #             Se "enciende" de modo ciclo de trabajo

            if DEBUG:
                print('Esperando', self._config.PAUSA, 'segundos')

            sleep(self._config.PAUSA)                                                   #     Se espera la pausa programada

            if DEBUG:
                print('Saliendo del modo de pruebas')


    def __del__(self):
        ''' Destructor de la clase: Ya que su ejecución no está asegurada, no hace nada
        '''

        pass


