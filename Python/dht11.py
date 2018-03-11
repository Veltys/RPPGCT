#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title             : dht11.py
# Description       : Módulo auxiliar para la gestión de la sonda de temperatura DHT11
# Author            : Veltys
# Original author   : szazo
# Date              : 11-03-2018
# Version           : 1.0.0
# Usage             : python3 dht11.py o from dht11 import
# Notes             : Este módulo está pensado para ser llamado desde otros módulos y no directamente, aunque si es llamado de esta forma, también hará su trabajo e informará al usuario de los valores del sensor

DEBUG = False
DEBUG_REMOTO = True
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

try:
    from config import dht11_config as config                                   # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

if DEBUG_REMOTO:
    import pydevd                                                               # Depuración remota

from time import sleep                                                          # Para hacer pausas

import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class dht11:                                                                    # Clase de gestión del sensor DHT11 para Raspberry Pi
    _sensor = 0

    def __init__(self, sensor):
        config.GPIOS[sensor]

        self._sensor = sensor


    def _bits_a_bytes(self, bits):
        byte = 0
        bytess = []

        for i in range(0, len(bits)):
            byte = byte << 1
            if (bits[i]):
                byte = byte | 1

            else:
                byte = byte | 0

            if ((i + 1) % 8 == 0):
                bytess.append(byte)

                byte = 0

        return bytess


    def _calcular_bits(self, longitudes):
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


    def _calcular_checksum(self, bytess):
        return bytess[0] + bytess[1] + bytess[2] + bytess[3] & 255


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
                if actual == GPIO.LOW:                                          # Tenemos la bajada inicial
                    estado = STATE_INIT_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_INIT_PULL_UP:
                if actual == GPIO.HIGH:                                         # Tenemos la subida inicial
                    estado = STATE_DATA_FIRST_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_FIRST_PULL_DOWN:
                if actual == GPIO.LOW:                                          # Tenemos la bajada inicial, lo siguiente será una subida
                    estado = STATE_DATA_PULL_UP

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_UP:
                if actual == GPIO.HIGH:                                         # Subida, la longitud de ésta estará determinada en función de si viene un 0 o un 1
                    longitud_actual = 0

                    estado = STATE_DATA_PULL_DOWN

                    continue

                else:
                    continue

            if estado == STATE_DATA_PULL_DOWN:
                if actual == GPIO.LOW:                                          # Bajada, almacenaremos la longitud del periodo previo de subida
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
        longitudes = self._procesar_datos(datos)

        # Si no coincide la congitud con el valor esperado, ha habido un fallo en la transmisión
        if len(longitudes) != LONGITUD_DATOS:
            return resultado_dht11(ERR_MISSING_DATA, 0, 0)

        else:
            # Calcular bits a partir de las longitudes
            bits = self._calcular_bits(longitudes)

            # Calcular bytes
            bytess = self._bits_a_bytes(bits)

            # Calcular comprobación y comprobar
            checksum = self._calcular_checksum(bytess)

            if bytess[4] != checksum:
                return resultado_dht11(ERR_CRC, 0, 0)

            else:
                return resultado_dht11(ERR_NO_ERROR, bytess[2], bytess[0])


class resultado_dht11:                                                          # Clase resultado devuelto por el método dht11.leer()
    error = ERR_NO_ERROR
    temperatura = -1
    humedad = -1

    def __init__(self, error, temperatura, humedad):
        self.error = error
        self.temperatura = temperatura
        self.humedad = humedad

    def valido(self):
        return self.error == ERR_NO_ERROR


def main(argv = sys.argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    GPIO.setmode(GPIO.BCM)                                                      # Establecemos el sistema de numeración BCM
    GPIO.setwarnings(DEBUG)                                                     # De esta forma alertará de los problemas sólo cuando se esté depurando

    for i in range(len(config.GPIOS)):
        try:
            sensor = dht11(i)

        except IndexError:
            print('Sensor', i, '-> No válido',)

        else:
            resultado = sensor.leer()

            j = 0

            while not resultado.valido() and j < config.LIMITE:
                if DEBUG:
                    print('Sensor', i, '-> Resultado no válido:', end = '', sep = ' ')

                    if resultado.error == ERR_MISSING_DATA:
                        print('sin datos')

                    else: # resultado.error == ERR_CRC
                        print('error de redundancia cíclica')

                sleep(config.PAUSA)

                resultado = sensor.leer()

                j = j + 1

            if resultado.valido():
                print('Sensor ', i, ' -> temperatura: ', resultado.temperatura, 'º C, humedad relativa: ', resultado.humedad, '%', sep = '')

            else:
                print('Sensor', i, '-> Imposible obtener un resultado válido en', config.LIMITE, 'intentos')

            del sensor

        GPIO.cleanup()                                                          # Devolvemos los pines a su estado inicial
if __name__ == '__main__':
    main(sys.argv)
