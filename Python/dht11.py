#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title             : dht11.py
# Description       : Sistema gestor de sonda de temperatura DHT11
# Author            : Veltys
# Original author   : szazo
# Date              : 18-11-2018
# Version           : 2.1.0
# Usage             : python3 dht11.py o from dht11 import
# Notes             : ...


DEBUG                       = False
DEBUG_REMOTO                = False
DEBUG_SENSOR                = False
ERR_NO_ERROR                = 0
ERR_MISSING_DATA            = 1
ERR_CRC                     = 2
LONGITUD_DATOS              = 40
STATE_INIT_PULL_DOWN        = 1
STATE_INIT_PULL_UP          = 2
STATE_DATA_FIRST_PULL_DOWN  = 3
STATE_DATA_PULL_UP          = 4
STATE_DATA_PULL_DOWN        = 5


import errno                                                                                                # Códigos de error
import os                                                                                                   # Funcionalidades varias del sistema operativo
import sys                                                                                                  # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                                           # Depuración remota

import RPi.GPIO as GPIO                                                                                     # Acceso a los pines GPIO

import comun                                                                                                # Funciones comunes a varios sistemas

from threading import Thread                                                                                # Capacidades multihilo
from time import sleep                                                                                      # Para hacer pausas

if DEBUG_REMOTO:
    from pydevd_file_utils import setup_client_server_paths                                                 # Configuración de las rutas Eclipse ➡

try:
    from config import dht11_config as config                                                               # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class dht11(comun.app):
    ''' Clase del sistema gestor de sonda de temperatura DHT11
    '''

    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Inicializa las variables
            - Llama al constructor de la clase padre
        '''

        self._argumentos = None

        self._hijos = []                                                                                    # Preparación de la lista contenedora de hijos

        super().__init__(config, nombre)


    def argumentos(self, argumentos = False):
        ''' Método "sobrecargado" gracias al parámetro "argumentos"
            - Para "argumentos" == "False"
                - Actúa como observador de la variable "_argumentos" de la clase
            - Para "argumentos" != "False"
                - Actúa como modificador de la variable "_argumentos" de la clase
        '''

        if not(argumentos):
            return self._argumentos

        else:
            self._argumentos = argumentos


    def bucle(self):
        ''' Realiza (en bucle no en este caso) las tareas asignadas a este sistema
        '''

        if len(self._argumentos) != 2 or self._argumentos[1] != '-h':
            argumentos = self.procesar_argumentos(self._argumentos)

            for i, _ in enumerate(self._config.GPIOS):                                                      # Se recorre la lista de puertos GPIO para ir generando los hijos
                if DEBUG:
                    print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

                self._hijos.append(Thread(target = main_hijos, args = ((i, argumentos, self._config),)))    #     Se prepara cada hijo y se configura

                if DEBUG:
                    print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

                self._hijos[i].start()                                                                      #     Se inicia cada hijo

        else:
            print('Uso:', argumentos[0], '''[opciones]
    
    Opciones:
        -h    Muestra esta pantalla
        -i    Información / listado de sensores
        -t    Mostrar la temperatura
        -m    Mostrar la humedad relativa
        -u    Mostrar las unidades y no solamente la magnitud
    
    Nota: invocar el programa sin parámetros equivale a invocarlo con todos excepto -h (-i -t -m -u)
''')

        self.cerrar()


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema
        '''

        for hijo in self._hijos:                                                                            # Se recorren los hijos
            hijo.join()                                                                                     #     Para esperar su finalización

        super().cerrar()                                                                                    # Llamada al método cerrar() de la clase padre


    @staticmethod                                                                                           # Método estático
    def procesar_argumentos(argumentos):
        ''' Procesado de los argumentos
        '''

        res = []

        if len(argumentos) == 1:
            for _ in range(4):
                res.append(True)

        else:
            if any('-i' in s for s in argumentos):
                res.append(True)

            else:
                res.append(False)

            if any('-t' in s for s in argumentos):
                res.append(True)

            else:
                res.append(False)

            if any('-m' in s for s in argumentos):
                res.append(True)

            else:
                res.append(False)

            if any('-u' in s for s in argumentos):
                res.append(True)

            else:
                res.append(False)

        return res


class dht11_hijos(comun.app):
    ''' Clase de los hijos del sistema gestor de sonda de temperatura DHT11
    '''

    def __init__(self, id_hijo, argumentos, config):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
        '''

        # super().__init__()                                                                                # La llamada al constructor de la clase padre está desactivada a propósito

        self._argumentos = argumentos
        self._config = config
        self._bloqueo = False
        self._estado_conexion = comun.estados_conexion.DESCONECTADO
        self._modo_apagado = False

        self._id_hijo = id_hijo

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tMi configuración es ", self._GPIOS, sep = '')
            print('Hijo  #', self._id_hijo, "\tDeberé escuchar en el puerto GPIO", self._GPIOS[0][0] , ' y conmutar el puerto GPIO', self._GPIOS[1][0], sep = '')


    @staticmethod                                                                                           # Método estático
    def _bits_a_bytes(bits):
        ''' Conversor de bits a bytes
        '''

        byte = 0
        bytess = []

        for i, bit in enumerate(bits):
            byte = byte << 1
            if bit:
                byte = byte | 1

            else:
                byte = byte | 0

            if (i + 1) % 8 == 0:
                bytess.append(byte)

                byte = 0

        return bytess


    @staticmethod                                                                                           # Método estático
    def _calcular_bits(longitudes):
        ''' Cáculo de bits dada una longitud
        '''

        mas_corta = 1000
        mas_larga = 0

        for longitud in longitudes:
            if longitud < mas_corta:
                mas_corta = longitud

            if longitud > mas_larga:
                mas_larga = longitud

        media = mas_corta + (mas_larga - mas_corta) / 2                                                     # Se usa la media para determinar si el periodo es largo o corto

        bits = []

        for longitud in longitudes:
            bit = False

            if longitud > media:
                bit = True

            bits.append(bit)

        return bits


    @staticmethod                                                                                           # Método estático
    def _calcular_checksum(bytess):
        ''' Cálculo de la suma de control
        '''

        return bytess[0] + bytess[1] + bytess[2] + bytess[3] & 255


    def _enviar_y_esperar(self, salida, pausa):
        ''' Envío del activador de la sonda y espera de la pausa para posteriormente recibir
        '''

        GPIO.output(self._config.GPIOS[self._id_hijo][0], salida)

        sleep(pausa)


    @staticmethod                                                                                           # Método estático
    def _procesar_datos(datos):
        ''' Procesado de los datos recibidos
        '''

        estado = STATE_INIT_PULL_DOWN

        longitudes = []                                                                                     # Contendrá las longitudes de los periodos de subida
        longitud_actual = 0                                                                                 # Contendrá la longitud del periodo previo

        for dato in datos:
            longitud_actual += 1

            if estado == STATE_INIT_PULL_DOWN:
                if dato == GPIO.LOW:                                                                        # Bajada inicial
                    estado = STATE_INIT_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_INIT_PULL_UP:
                if dato == GPIO.HIGH:                                                                       # Subida inicial
                    estado = STATE_DATA_FIRST_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_FIRST_PULL_DOWN:
                if dato == GPIO.LOW:                                                                        # Bajada inicial, lo siguiente será una subida
                    estado = STATE_DATA_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_UP:
                if dato == GPIO.HIGH:                                                                       # Subida, la longitud de ésta estará determinada en función de si viene un 0 o un 1
                    longitud_actual = 0

                    estado = STATE_DATA_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_DOWN:
                if dato == GPIO.LOW:                                                                        # Bajada, almacenaremos la longitud del periodo previo de subida
                    longitudes.append(longitud_actual)

                    estado = STATE_DATA_PULL_UP

                    continue

                else:
                    continue

        return longitudes


    def _recoger_datos(self):
        ''' Recogida de los datos
        '''

        continuo = 0                                                                                        # Recopilar datos hasta que se encuentre un continuo
        datos = []
        max_continuo = 100                                                                                  # Usado para determinar el final de los datos
        ultimo = -1


        while True:
            actual = GPIO.input(self._config.GPIOS[self._id_hijo][0])

            datos.append(actual)

            if ultimo != actual:
                continuo = 0
                ultimo = actual

            else:
                continuo += 1

                if continuo > max_continuo:
                    break

        return datos


    def bucle(self):
        ''' Realiza (en bucle no, en este caso) las tareas asignadas a este sistema
        '''

        resultado = self.leer()

        j = 0

        if not DEBUG_SENSOR:
            while not resultado.valido() and j < config.LIMITE:
                if DEBUG:
                    print('Sensor', self._id_hijo, '-> Resultado no válido: ', end = '', sep = ' ')

                    if resultado.error == ERR_MISSING_DATA:
                        print('sin datos')

                    else: # resultado.error == ERR_CRC
                        print('error de redundancia cíclica')

                sleep(config.PAUSA)

                resultado = self.leer()

                j = j + 1

        if DEBUG_SENSOR or resultado.valido():
            if self._argumentos[0]:                                                                         # Información del sensor
                print('Sensor', self._id_hijo, '-> ', end = '')

            if self._argumentos[0] and not self._argumentos[1] and not self._argumentos[2]:
                print('operativo', end = '')

            if self._argumentos[0] and self._argumentos[1]:
                print('t', end = '')

            elif self._argumentos[1]:
                print('T', end = '')

            if self._argumentos[1]:                                                                         # Temperatura
                print('emperatura:', resultado.temperatura, end = '')

            if self._argumentos[1] and self._argumentos[3]:                                                 # Unidades
                print('º C', end = '')

            if self._argumentos[1] and self._argumentos[2]:
                print(', ', end = '')

            if (self._argumentos[0] or self._argumentos[1]) and self._argumentos[2]:
                print('h', end = '')

            elif self._argumentos[2]:
                print('H', end = '')

            if self._argumentos[2]:                                                                         # Humedad
                print('umedad relativa:', resultado.humedad, end = '')

            if self._argumentos[2] and self._argumentos[3]:
                print('%', end = '')

            print("\n")

        else:
            print('Sensor', self._id_hijo, '-> Imposible obtener un resultado válido en', config.LIMITE, 'intentos')

        del resultado


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema
        '''

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tDisparado el evento de cierre", sep = '')

        # super().cerrar()                                                                                  # La llamada al método de cierre de la clase padre está desactivada a propósito


    def leer(self):
        ''' Lee datos del sensor
        '''

        GPIO.setup(self._config.GPIOS[self._id_hijo][0], GPIO.OUT)                                          # Modo de escritura

        self._enviar_y_esperar(GPIO.HIGH, 0.05)                                                             # Señal de lectura

        self._enviar_y_esperar(GPIO.LOW, 0.02)                                                              # Fin de la señal de lectura

        GPIO.setup(self._config.GPIOS[self._id_hijo][0], GPIO.IN, GPIO.PUD_UP)                              # Cambiando a modo lectura

        datos = self._recoger_datos()                                                                       # Recibiendo datos

        longitudes = self._procesar_datos(datos)                                                            # Procesamiento de datos

        if len(longitudes) != LONGITUD_DATOS:                                                               # Si no coincide la congitud con el valor esperado, ha habido un fallo en la transmisión
            return resultado_dht11(ERR_MISSING_DATA, 0, 0)

        else:
            bits = self._calcular_bits(longitudes)                                                          # Calcular bits a partir de las longitudes

            bytess = self._bits_a_bytes(bits)                                                               # Calcular bytes

            checksum = self._calcular_checksum(bytess)                                                      # Calcular comprobación y comprobar

            if bytess[4] != checksum:
                return resultado_dht11(ERR_CRC, 0, 0)

            else:
                temperatura = bytess[2] + float(bytess[3]) / 10

                humedad = bytess[0] + float(bytess[1]) / 10

                return resultado_dht11(resultado_dht11.ERR_NO_ERROR, temperatura, humedad)


class resultado_dht11:                                                          	                        # Clase resultado devuelto por el método dht11.leer()
    error = ERR_NO_ERROR
    temperatura = -1
    humedad = -1

    def __init__(self, error, temperatura, humedad):
        self.error = error
        self.temperatura = temperatura
        self.humedad = humedad


    def valido(self):
        return self.error == ERR_NO_ERROR


def main(argv):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA, trace_only_current_thread = False)

    app = dht11(config, os.path.basename(argv[0]))

    err = app.arranque()

    if err == 0:
        app.argumentos(argv)
        app.bucle()

    else:
        sys.exit(err)


def main_hijos(argv):
    app = dht11_hijos(argv[0], argv[1], argv[2])

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
