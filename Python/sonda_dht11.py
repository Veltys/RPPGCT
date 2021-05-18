#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title             : sonda_dht11.py
# Description       : Sistema gestor de sonda de temperatura DHT11
# Author            : Veltys
# Date              : 2021-04-30
# Version           : 3.0.0
# Usage             : python3 sonda_dht11.py o from sonda_dht11 import
# Notes             : ...


DEBUG           = False
DEBUG_HIJOS     = False
DEBUG_REMOTO    = False
DEBUG_SENSOR    = False


import errno                                                                                                    # Códigos de error
import os                                                                                                       # Funcionalidades varias del sistema operativo
import sys                                                                                                      # Funcionalidades varias del sistema
from threading import Thread                                                                                    # Capacidades multihilo
from time import sleep                                                                                          # Para hacer pausas

import RPi.GPIO as GPIO                                                                                         # Acceso a los pines GPIO
import comun                                                                                                    # Funciones comunes a varios sistemas
import dht11                                                                                                    # Acceso a sondas de temperatura y humedad DHT11

if DEBUG:
    import inspect                                                                                              # Metaprogramación

if DEBUG_REMOTO:
    import pydevd                                                                                               # Depuración remota
    from pydevd_file_utils import setup_client_server_paths                                                     # Configuración de las rutas Eclipse ➡

try:
    from config import dht11_config as config                                                                   # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class sonda_dht11(comun.app):
    ''' Clase del sistema gestor de sonda de temperatura DHT11
    '''

    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Inicializa las variables
            - Llama al constructor de la clase padre
        '''

        self._argumentos = None

        self._hijos = []                                                                                        # Preparación de la lista contenedora de hijos

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
        ''' Realiza (en bucle no, en este caso) las tareas asignadas a este sistema
        '''

        # TODO: Cambiar el procesador de argumentos por argparse.ArgumentParser()
        if len(self._argumentos) != 2 or self._argumentos[1] != '-h':
            argumentos = self.procesar_argumentos(self._argumentos)

            for i, _ in enumerate(self._config.SONDAS):                                                         # Se recorre la lista de sondas para ir generando los hijos
                if DEBUG:
                    print(f"Padre #{os.getpid()}\tPreparando hijo {i}")

                if not DEBUG_HIJOS:
                    self._hijos.append(Thread(target = main_hijos, args = ((i, argumentos, self._config),)))    #     Se prepara cada hijo y se configura

                if DEBUG:
                    print(f"Padre #{os.getpid()}\tArrancando hijo {i}")

                if not DEBUG_HIJOS:
                    self._hijos[i].start()                                                                      #     Se inicia cada hijo

                else:
                    main_hijos([i, argumentos, self._config])

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

        for hijo in self._hijos:                                                                                # Se recorren los hijos
            hijo.join()                                                                                         #     Para esperar su finalización

        super().cerrar()                                                                                        # Llamada al método cerrar() de la clase padre


    @staticmethod                                                                                               # Método estático
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


class sonda_dht11_hijos(comun.app):
    ''' Clase de los hijos del sistema gestor de sonda de temperatura DHT11
    '''

    def __init__(self, id_hijo, argumentos, config):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
        '''

        # super().__init__()                                                                                    # La llamada al constructor de la clase padre está desactivada a propósito

        self._argumentos = argumentos
        self._config = config
        self._bloqueo = False
        self._estado_conexion = comun.estados_conexion.DESCONECTADO
        self._modo_apagado = False

        self._id_hijo = id_hijo

        if DEBUG:
            print(f"Hijo  #{self._id_hijo}\tMi configuración es:")

            for metodo in inspect.getmembers(self._config):
                if not metodo[0].startswith('_'):
                    if not inspect.ismethod(metodo[1]):
                        print(metodo)

            print(f"Hijo  #{self._id_hijo}\tDeberé trabajar en el puerto GPIO{self._config.SONDAS[self._id_hijo]}")


    def bucle(self):
        ''' Realiza (en bucle no, en este caso) las tareas asignadas a este sistema
        '''

        resultado = self.leer()

        ejecuciones = 0

        if not DEBUG_SENSOR:
            while not resultado.is_valid() and ejecuciones < config.LIMITE:
                if DEBUG:
                    print(f'Sensor {self._id_hijo} ➡️ Resultado no válido: ', end = '')

                    if resultado.error_code == dht11.DHT11Result.ERR_MISSING_DATA:
                        print('sin datos')

                    else: # resultado.error == ERR_CRC
                        print('error de redundancia cíclica')

                sleep(config.PAUSA)

                resultado = self.leer()

                ejecuciones += 1

        if DEBUG_SENSOR or resultado.valido():
            if self._argumentos[0]: # Información del sensor
                print(f'Sensor {self._id_hijo} ➡️ ', end = '')

            if self._argumentos[0] and not self._argumentos[1] and not self._argumentos[2]:
                print('operativo', end = '')

            if self._argumentos[0] and self._argumentos[1]:
                print('t', end = '')

            elif self._argumentos[1]:
                print('T', end = '')

            if self._argumentos[1]:                                                                             # Temperatura
                print(f'emperatura: {resultado.temperature}', end = '')

            if self._argumentos[1] and self._argumentos[3]:                                                     # Unidades
                print('º C', end = '')

            if self._argumentos[1] and self._argumentos[2]:
                print(', ', end = '')

            if (self._argumentos[0] or self._argumentos[1]) and self._argumentos[2]:
                print('h', end = '')

            elif self._argumentos[2]:
                print('H', end = '')

            if self._argumentos[2]:                                                                             # Humedad
                print(f'umedad relativa: {resultado.humidity}', end = '')

            if self._argumentos[2] and self._argumentos[3]:
                print('%', end = '')

            print("\n")

        else:
            print(f'Sensor {self._id_hijo} ➡️ Imposible obtener un resultado válido en {config.LIMITE} intentos')

        # del resultado


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema
        '''

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tDisparado el evento de cierre", sep = '')

        # super().cerrar()                                                                                      # La llamada al método de cierre de la clase padre está desactivada a propósito


    def leer(self):
        ''' Lee datos del sensor
        '''

        return dht11.DHT11(pin = self._config.SONDAS[self._id_hijo]).read()


def main(argv):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA, trace_only_current_thread = False)

    app = sonda_dht11(config, os.path.basename(argv[0]))

    err = app.arranque()

    if err == 0:
        # Inicialización de los puertos GPIO, ya que no es posible hacerlo en el arranque
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        app.argumentos(argv)
        app.bucle()

    else:
        sys.exit(err)


def main_hijos(argv):
    app = sonda_dht11_hijos(argv[0], argv[1], argv[2])

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
