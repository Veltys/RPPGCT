#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : dht11_servidor.py
# Description   : Parte servidor del sistema gestor de la sonda de temperatura DHT11
# Author        : Veltys
# Date          : 05-03-2018
# Version       : 1.0.0
# Usage         : python3 domotica_dht11.py
# Notes         : Parte servidor del sistema en el que se gestionará la sonda de temperatura DHT11


DEBUG = True
DEBUG_PADRE = False
DEBUG_REMOTO = True


salir = False                                                                   # Ya que no es posible matar a un hilo, esta "bandera" global servirá para indicarle a los hilos que deben terminar


import errno                                                                    # Códigos de error
import sys                                                                      # Funcionalidades varias del sistema
import os                                                                       # Funcionalidades varias del sistema operativo

try:
    from config import dht11_servidor_config as config                          # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from threading import Lock, Thread                                              # Capacidades multihilo
from time import sleep                                                          # Para hacer pausas
import comun                                                                    # Funciones comunes a varios sistemas

if DEBUG_REMOTO:
    import pydevd                                                               # Depuración remota

import socket                                                                   # Tratamiento de sockets
import RPi.GPIO as GPIO                                                         # Acceso a los pines GPIO


class dht11_servidor(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

        self._datos = []
        self.datos = []



        bits_min = 999;
        bits_max = 0;
        HumidityBit = ''
        TemperatureBit = ''
        crc = ''
        Humidity = 0
        Temperature = 0


    def bucle(self):
        try:
            while True:
                self._recibir_datos()
                self._analizar_datos()

                if(self._validar_datos()):
                    self._almacenar_datos()

                    sleep(self._config.PAUSA)

                else:
                    sleep(2);

        except KeyboardInterrupt:
            self.cerrar()
            return


    def _recibir_datos(self):
        for i in range(len(self._config.GPIOS_1Wire)):
            if DEBUG:
                print('Proceso  #', os.getpid(), "\tPreparando el puerto GPIO", self._config.GPIOS_1Wire[i][0], sep = '')

            GPIO.setup(self._config.GPIOS_1Wire[i][0], GPIO.OUT)

            if DEBUG:
                print('Proceso  #', os.getpid(), "\tEnviando señal de lectura en el puerto GPIO", self._config.GPIOS_1Wire[i][0], ' con el protocolo 1 Wire', sep = '')

            GPIO.output(self._config.GPIOS_1Wire[i][0], GPIO.HIGH)

            sleep(0.025)

            if DEBUG:
                print('Proceso  #', os.getpid(), "\tEnviada señal de lectura en el puerto GPIO", self._config.GPIOS_1Wire[i][0], ' con el protocolo 1 Wire', sep = '')

            GPIO.output(self._config.GPIOS_1Wire[i][0], GPIO.LOW)

            sleep(0.14)

            if DEBUG:
                print('Proceso  #', os.getpid(), "\tReconfigurando el puerto GPIO", self._config.GPIOS_1Wire[i][0], ' para lectura', sep = '')

            GPIO.setup(self._config.GPIOS_1Wire[i][0], GPIO.IN, pull_up_down = GPIO.PUD_UP)

            self._datos.append([])

            for j in range(0, 1000):
                self._datos[i].append(GPIO.input(self._config.GPIOS_1Wire[i][0]))


    def __del__(self):
        super().__del__()

pin = 16


GPIO.setmode(GPIO.BCM)




class dht11_servidor_hijos(comun.app):
    pass


def main(argv = sys.argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = dht11_servidor(config, os.path.basename(sys.argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


def main_hijos(argv):
    app = dht11_servidor_hijos(argv, config)
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)















'''
def bin2dec(string_num):
    return str(int(string_num, 2))

def analyzeData():
# {{{ Analyze data

# {{{ Add HI (2x8)x3 bits to array

    seek = 0;
    bits_min = 9999;
    bits_max = 0;

    global HumidityBit
    global TemperatureBit
    global crc
    global Humidity
    global Temperature

    HumidityBit = ""
    TemperatureBit = ""
    crc = ""

    """
    Snip off the first bit - it simply says "Hello, I got your request, will send you temperature and humidity information along with checksum shortly"
    """
    while(seek < len(data) and data[seek] == 0):
        seek += 1;

    while(seek < len(data) and data[seek] == 1):
         seek += 1;

    """
    Extract all HIGH bits' blocks. Add each block as separate item in data[] 
    """
    for i in range(0, 40):

        buffer = "";

        while(seek < len(data) and data[seek] == 0):
            seek += 1;


        while(seek < len(data) and data[seek] == 1):
            seek += 1;
            buffer += "1";

        """
        Find the longest and the shortest block of HIGHs. Average of those two will distinct whether block represents '0' (shorter than avg) or '1' (longer than avg)
        """

        if (len(buffer) < bits_min):
            bits_min = len(buffer)

        if (len(buffer) > bits_max):
            bits_max = len(buffer)

        effectiveData.append(buffer);
        # print "%s " % buffer

# }}}



# {{{ Make effectiveData smaller

    """
    Replace blocks of HIs with either '1' or '0' depending on block length
    """
    for i in range(0, len(effectiveData)):
        if (len(effectiveData[i]) < ((bits_max + bits_min) / 2)):
            effectiveData[i] = "0";
        else:
            effectiveData[i] = "1";

        # print "%s " % effectiveData[i],
   # print


# }}}


# {{{ Extract Humidity and Temperature values

    for i in range(0, 8):
        HumidityBit += str(effectiveData[i]);

    for i in range(16, 24):
        TemperatureBit += str(effectiveData[i]);


    for i in range(32, 40):
        crc += str(effectiveData[i]);

    Humidity = bin2dec(HumidityBit)
    Temperature = bin2dec(TemperatureBit)

    # print "HumidityBit=%s, TemperatureBit=%s, crc=%s" % (HumidityBit, TemperatureBit, crc)

# }}}

# }}}


# {{{ Check CRC
def isDataValid():

    global Humidity
    global Temperature
    global crc

    # print "isDataValid(): H=%d, T=%d, crc=%d"% (int(Humidity), int(Temperature), int(bin2dec(crc)))
    if int(Humidity) + int(Temperature) == int(bin2dec(crc)):
        return True;
    else:
        return False;
# }}}


# {{{ Print data
def printData():
   global Humidity
   global Temperature

   print('H: ', Humidity)
   print('T: ', Temperature)
# }}}
'''
