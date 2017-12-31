#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import RPi.GPIO as GPIO                                                             # Importamos las librerias necesarias para usar los pines GPIO
from time import sleep                                                              # Importamos time para poder realizar pausas

def bin2dec(string_num):                                                            # Creamos una funcion para transformar de binario a decimal
    return str(int(string_num, 2))

data = []                                                                           # Definimos data como un array

GPIO.setmode(GPIO.BCM)                                                              # Ponemos la placa en modo BCM
GPIO.setup(16, GPIO.OUT)                                                            # Configuramos el pin 4 como salida
GPIO.output(16 , GPIO.HIGH)                                                          # Enviamos una señal
sleep(0.025)                                                                        # Pequeña pausa
GPIO.output(16 , GPIO.LOW)                                                           # Cerramos la señal
sleep(0.02)                                                                         # Pequeña pausa

GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_UP)                                   # Ponemos el pin 4 en modo lectura

for i in range(0, 500):                                                             # Lee los bits que conforman la respuesta binaria del sensor
    data.append(GPIO.input(16))

# Define algunas variables usadas para cálculos más adelante
bit_count = 0
tmp = 0
count = 0
HumidityBit = ""
TemperatureBit = ""
crc = ""

''' Hazlo mientras no existan errores, si detectas error salta a "except"
    El siguiente código lee los bits de respuesta que envia el
    sensor y los transforma a un número decimal leíble.
'''
try:
    while data[count] == 1:
        tmp = 1
        count = count + 1

    for i in range(0, 32):
        bit_count = 0

        while data[count] == 0:
            tmp = 1
            count = count + 1

        while data[count] == 1:
            bit_count = bit_count + 1
            count = count + 1

        if bit_count > 3:
            if i >= 0 and i < 8:
                HumidityBit = HumidityBit + "1"
            if i >= 16 and i < 24:
                TemperatureBit = TemperatureBit + "1"
        else:
            if i >= 0 and i < 8:
                HumidityBit = HumidityBit + "0"
            if i >= 16 and i < 24:
                TemperatureBit = TemperatureBit + "0"

except:
    print('ERR_RANGE')

    exit(0)

try:
    for i in range(0, 8):
        bit_count = 0

        while data[count] == 0:
            tmp = 1
            count = count + 1

        while data[count] == 1:
            bit_count = bit_count + 1
            count = count + 1

        if bit_count > 3:
            crc = crc + "1"

        else:
            crc = crc + "0"
except:                                                                             # Errores en el bloque
    print('ERR_RANGE')

    exit(0)                                                                         # Salimos

# Aquí obtendríamos las lecturas de humedad y temperatura en un formato mas manejable
Humidity = bin2dec(HumidityBit)
Temperature = bin2dec(TemperatureBit)

if int(Humidity) + int(Temperature) - int(bin2dec(crc)) == 0:                       # La comprobacion del CRC se ha validado
    print('Humidity: ', Humidity, '%')
    print('Temperature: ', Temperature, 'C')

else:                                                                               # Si no es valido
    print('ERR_CRC')
