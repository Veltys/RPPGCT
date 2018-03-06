#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from psutil._compat import long


# Title             : dht11.py
# Description       : Módulo auxiliar para la gestión de la sonda de temperatura DHT11
# Author            : Veltys
# Original author   : szazo
# Date              : 05-03-2018
# Version           : 1.0.0
# Usage             : python3 dht11.py o from dht11 import
# Notes             : Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de los valores del sensor


DEBUG = True
LONGITUD_DATOS = 40                                                             # 4 bytes de datos + 1 byte de comprobación = 5 * 8 = 40

ERR_NO_ERROR = 0
ERR_MISSING_DATA = 1
ERR_CRC = 2


STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema
import os                                                                       # Funcionalidades varias del sistema operativo

try:
    from config import dht11_config as config                                   # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from time import sleep                                                          # Para hacer pausas

import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class dht11:
    # Clase de gestión del sensor DHT11 para Raspberry Pi

    _sensor = 0

    def __init__(self, sensor):
        config.GPIOS[sensor]

        self._sensor = sensor


    def _bits_a_bytes(self, bits):
        byte = 0
        bytes = []

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1

            else:
                byte = byte | 0

            if ((i + 1) % 8 == 0):
                bytes.append(byte)

                byte = 0

        return bytes


    def __calcular_bits(self, longitudes):
        mas_corta = 1000
        mas_larga = 0

        for i in range(0, len(longitudes)):
            longitud = longitudes[i]

            if longitud < mas_corta:
                mas_corta = longitud

            if longitud > mas_larga:
                mas_larga = longitud

        # Se usa la media para determinar si el periodo es largo o corto
        media = mas_corta + (mas_larga - mas_corta) / 2

        bits = []

        for i in range(0, len(longitudes)):
            bit = False

            if longitudes[i] > media:
                bit = True

            bits.append(bit)

        return bits


    def __calcular_checksum(self, bytes):
        return bytes[0] + bytes[1] + bytes[2] + bytes[3] & 255


    def _enviar_y_esperar(self, salida, pausa):
        GPIO.output(config.GPIOS[self._sensor][0], salida)

        sleep(pausa)


    def _procesar_datos(self, datos):
        estado = STATE_INIT_PULL_DOWN

        longitudes = []                                                         # Contendrá las longitudes de los periodos de subida
        longitud_actual = 0                                                     # Contendrá la longitud del periodo previo

        for i in range(len(datos)):
            actual = datos[i]
            longitud_actual += 1

            if estado == STATE_INIT_PULL_DOWN:
                if actual == RPi.GPIO.LOW:                                      # Tenemos la bajada inicial
                    estado = STATE_INIT_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_INIT_PULL_UP:
                if actual == RPi.GPIO.HIGH:                                     # Tenemos la subida inicial
                    estado = STATE_DATA_FIRST_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_FIRST_PULL_DOWN:
                if actual == RPi.GPIO.LOW:                                      # Tenemos la bajada inicial, lo siguiente será una subida
                    estado = STATE_DATA_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_UP:
                if actual == RPi.GPIO.HIGH:                                     # Subida, la longitud de ésta estará determinada en función de si viene un 0 o un 1
                    actual_length = 0

                    estado = STATE_DATA_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_DOWN:
                if actual == RPi.GPIO.LOW:                                      # Bajada, almacenaremos la longitud del periodo previo de subida
                    longitudes.append(longitud_actual)

                    estado = STATE_DATA_PULL_UP

                    continue

                else:
                    continue

        return longitudes


    def _recoger_datos(self):
        continuo = 0                                                            # Recopilar datos hasta que se encuentre un continuo
        datos = []
        max_continuo = 100                                                      # Usado para determinar el final de los datos
        ultimo = -1


        while True:
            actual = GPIO.input(config.GPIOS[self._sensor][0])

            datos.append(actual)

            if ultimo != actual:
                continuo = 0
                ultimo = actual

            else:
                continuo += 1

                if continuo > max_continuo:
                    break

        return datos


    def leer(self):
        # Modo de escritura
        GPIO.setup(config.GPIOS[self._sensor][0], GPIO.OUT)

        # Señal de lectura
        self._enviar_y_esperar(GPIO.HIGH, 0.05)

        # Fin de la señal de lectura
        self._enviar_y_esperar(GPIO.LOW, 0.02)

        # Cambiando a modo lectura
        GPIO.setup(config.GPIOS[self._sensor][0], GPIO.IN, GPIO.PUD_UP)

        # Recibiendo datos
        datos = self._recoger_datos()

        # Procesamiento de datos
        longitudes = self._procesar_datos(data)

        # Si no coincide la congitud con el valor esperado, ha habido un fallo en la transmisión
        if len(longitudes) != LONGITUD_DATOS:
            return resultado_dht11(ERR_MISSING_DATA, 0, 0)

        else:
            # Calcular bits a partir de las longitudes
            bits = self._calcular_bits(longitudes)

            # Calcular bytes
            bytes = self._bits_a_bytes(bits)

            # Calcular comprobación y comprobar
            checksum = self._calcular_checksum(bytes)

            if bytes[4] != checksum:
                return resultado_dht11(ERR_CRC, 0, 0)

            else:
                return resultado_dht11(ERR_NO_ERROR, bytes[2], bytes[0])


class resultado_dht11:
    # Clase resultado devuelto por el método dht11.leer()

    error = ERR_NO_ERROR
    temperatura = -1
    humedad = -1

    def __init__(self, error, temperatura, humedad):
        self.error = error
        self.temperatura = temperatura
        self.humedad = humedad

    def valido(self):
        return self.error == DHT11Result.ERR_NO_ERROR


def main(argv = sys.argv):
    try:
        sensor = dht11(0)

    except AttributeError:
        resultado = sensor.leer()

        while not resultado.valido():
            resultado = sensor.leer()

            sleep(config.PAUSA)

        print('Temperatura: ', resultado.temperatura, 'º C, humedad relativa: ', resultado.humedad, '%', sep = '')

    else:
        print('El sensor selccionado no es válido')


if __name__ == '__main__':
    main(sys.argv)
