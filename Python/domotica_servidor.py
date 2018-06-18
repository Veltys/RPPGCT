#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_servidor.py
# Description   : Parte servidor del sistema gestor de domótica
# Author        : Veltys
# Date          : 24-05-2018
# Version       : 2.0.0
# Usage         : python3 domotica_servidor.py
# Notes         : Parte servidor del sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


DEBUG           = True
DEBUG_PADRE     = False
DEBUG_REMOTO    = True


salir           = False                                                                                                                       # Ya que no es posible matar a un hilo, esta "bandera" global servirá para indicarle a los hilos que deben terminar
semaforo        = Lock()                                                                                                                   # Un semáforo evitará que el padre y los hijos den problemas al acceder a una variable que ambos puedan modificar


import errno                                                                                                                        # Códigos de error
import os                                                                                                                           # Funcionalidades varias del sistema operativo
import socket                                                                                                                       # Tratamiento de sockets
import sys                                                                                                                          # Funcionalidades varias del sistema

import comun                                                                                                                        # Funciones comunes a varios sistemas

if DEBUG_REMOTO:
    import pydevd                                                                                                                   # Depuración remota

import RPi.GPIO as GPIO                                                                                                             # Acceso a los pines GPIO

from subprocess import call                                                                                                         # Lanzamiento de nuevos procesos
from threading import Lock, Thread                                                                                                  # Capacidades multihilo
from time import sleep                                                                                                              # Para hacer pausas

try:
    from config import domotica_servidor_config as config                                                                           # Configuración


class domotica_servidor(comun.app):
    def __init__(self, config, nombre):
        super().__init__(config, nombre)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind(('127.0.0.1', self._config.puerto))                                                                       # TODO: IPv6
        self._socket.listen(1)                                                                                                      # No se preveen muchas conexiones, así que, por ahora, se soportará solamente un cliente


    def apagar(self, puerto, modo = False):
        global semaforo

        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            with semaforo:                                                                                                          # Para realizar el apagado es necesaria un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], GPIO.LOW if self._config.GPIOS[puerto][2] else GPIO.HIGH)                # Se desactiva la salida del puerto GPIO

            return True

        else:
            return False


    def bucle(self):
        try:
            if DEBUG:
                print('Padre #', os.getpid(), "\tMi configuración es: ", self._config.GPIOS, sep = '')
                print('Padre #', os.getpid(), "\tPienso iniciar ", int(len(self._config.GPIOS) / 2), ' hijos', sep = '')

            if not(DEBUG_PADRE):
                self._hijos = list()
                for i in range(int(len(self._config.GPIOS) / 2)):
                    if DEBUG:
                        print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

                    self._hijos.append(Thread(target = main_hijos, args = (i,)))

                    if DEBUG:
                        print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

                    self._hijos[i].start()

            while True:
                sc, _ = self._socket.accept()
                comando = sc.recv(1024)
                comando = comando.decode('utf_8')
                comando = comando.lower()

                if DEBUG:
                    print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

                while comando[0:11] != 'desconectar':
                    # listar
                    if comando == 'listar':
                        mensaje = 'info: '

                        for i in range(0, int(len(self._config.GPIOS)), 2):
                            mensaje = mensaje + str(self._config.GPIOS[i + 1][0]) + ' '

                        if DEBUG:
                            print('Padre #', os.getpid(), "\tVoy a mandarle el mensaje: ", mensaje, sep = '')

                    # conmutar, pulsar, encender, apagar
                    elif (comando != 'apagar'       and comando[:6] == 'apagar'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (comando != 'conmutar'     and comando[:8] == 'conmutar'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (comando != 'describir'    and comando[:9] == 'describir'  and comando[9] == ' ' and comando[10:] != '') \
                      or (comando != 'encender'     and comando[:8] == 'encender'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (comando != 'estado'       and comando[:6] == 'estado'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (comando != 'hola'         and comando[:4] == 'hola'       and comando[4] == ' ' and comando[ 5:] != '') \
                      or (comando != 'pulsar'       and comando[:6] == 'pulsar'     and comando[6] == ' ' and comando[ 7:] != '') \
                    :
                        (funcion, params) = comando.split(' ', 1)

                        try:
                            respuesta = eval('self.' + funcion + '(' + params + ')')

                        except AttributeError:
                            if DEBUG:
                                print('Padre #', os.getpid(), "\tEl comando \"" + comando + '" es incorrecto o no está implementado', sep = '')

                            mensaje = 'err: incorrecto o no implementado'
                            sc.send(mensaje.encode('utf_8'))

                        else:
                            if comando[:4] == 'hola':
                                mensaje = respuesta

                            elif comando[:6] != 'estado' and comando[:9] != 'describir' and respuesta:
                                mensaje = 'ok: ejecutado'

                            elif (comando[:6] == 'estado' and respuesta != -1) or (comando[0:9] == 'describir' and respuesta != False):
                                mensaje = 'info: ' + str(respuesta)

                            else:
                                mensaje = 'err: no ejecutado, puerto incorrecto o no encontrado'

                    else:
                        mensaje = 'err: no ejecutado, comando incorrecto'

                    try:
                        sc.send(mensaje.encode('utf_8'))

                    except BrokenPipeError:
                        comando = 'desconectar'

                    except ConnectionResetError:
                        comando = 'desconectar'

                    else:
                        try:
                            comando = sc.recv(1024)

                        except ConnectionResetError:
                            comando = 'desconectar'

                        else:
                            comando = comando.decode('utf_8')
                            comando = comando.lower()

                    finally:
                        if DEBUG:
                            print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

                if comando[0:5] == 'desconectar':
                    sc.close()

        except KeyboardInterrupt:
            self.cerrar()
            return


    def buscar_puerto_GPIO(self, puerto):
        if isinstance(puerto, int) and puerto > 0 and puerto <= 27:                                                                 # 27 es el número de puertos GPIO que tiene una Raspberry Pi
            for i in range(1, int(len(self._config.GPIOS)), 2):                                                                     # Se buscará a lo largo de self._config.GPIOS...
                if self._config.GPIOS[i][0] == puerto:                                                                              # ... si hay una coincidencia con el puerto pedido
                    return i                                                                                                        # De haberla, se retornará el orden en el que se encuentra

        return -1                                                                                                                   # Si se llega aquí, será que no hay coincidencias, por lo cual, se indicará también


    def cerrar(self):
        global salir

        salir = True

        if DEBUG:
            print('Padre #', os.getpid(), "\tDisparado el evento de cierre", sep = '')

        if not(DEBUG_PADRE):
            for hijo in self._hijos:
                hijo.join()

        super().cerrar()


    def conmutar(self, puerto, modo = False):
        global semaforo

        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            with semaforo:                                                                                                          # Para realizar la conmutación es necesaria un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], not(GPIO.input(self._config.GPIOS[puerto][0])))                          # Se conmuta la salida del puerto GPIO

            return True

        else:
            return False


    def describir(self, puerto, modo = False):
        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            return self._config.GPIOS[puerto][4]

        else:
            return False


    def encender(self, puerto, modo = False):
        global semaforo

        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            with semaforo:                                                                                                          # Para realizar el encendido es necesaria un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], GPIO.HIGH if self._config.GPIOS[puerto][2] else GPIO.LOW)                # Se activa la salida del puerto GPIO

            return True

        else:
            return False


    # TODO: Mejora de calidad
    def estado(self, puerto, modo = False):
        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            return GPIO.input(self._config.GPIOS[puerto][0])

        else:
            return -1


    def hola(self, version):
        test = self._VERSION_PROTOCOLO - float(version)                                                                             # Evaluaremos ambas versiones (la nuestra y la del cliente) con una simple resta de "floats"

        if test < 0:                                                                                                                # Si nuestra versión es superior...
            self._VERSION_PROTOCOLO = float(version)                                                                                # ... nos adaptamos...

            return 'Ok: ' + str(version)                                                                                            # ... y damos el OK

        elif test == 0:                                                                                                             # Si nuestra versión es la misma
            return 'Ok: ' + str(version)                                                                                            # ... damos el OK

        else:                                                                                                                       # Si nuestra versión es inferior...
            return 'Info: ' + str(self._VERSION_PROTOCOLO)                                                                          # ... pedimos que se adapte el cliente


    def pulsar(self, puerto, modo = False):
        if modo == False:
            puerto = self.buscar_puerto_GPIO(puerto)

        if puerto != -1:
            correcto = True
            correcto = correcto and self.encender(puerto, True)

            sleep(2)

            correcto = correcto and self.apagar(puerto, True)

            return correcto

        else:
            return False


    def __del__(self):
        super().__del__()


class domotica_servidor_hijos(comun.app):
    def __init__(self, id_hijo, config):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
        '''

        # super().__init__()                                                                                                        # La llamada al constructor de la clase padre está comentada a propósito

        self._config = config
        self._bloqueo = False
        self._estado = 0
        self._modo_apagado = False

        self._id_hijo = id_hijo

        self._GPIOS = list()
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2])
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2 + 1])

        self._LLAMADAS = self._config.LLAMADAS[self._id_hijo]

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tMi configuración es ", self._GPIOS, sep = '')
            print('Hijo  #', self._id_hijo, "\tDeberé escuchar en el puerto GPIO", self._GPIOS[0][0] , ' y conmutar el puerto GPIO', self._GPIOS[1][0], sep = '')


    def arranque(self):
        # super().arranque()                                                                                                        # La llamada al método de la clase padre está comentada a propósito

        return 0                                                                                                                    # En este caso, no es necesario realizar operaciones de arranque, ya que el hilo padre las ha realizado todas


    def bucle(self):
        global semaforo, salir

        try:
            GPIO.add_event_detect(self._GPIOS[0][0], GPIO.BOTH)                                                                     # Se añade el evento; se ha empleado GPIO.BOTH porque GPIO.RISING y GPIO.FALLING no parecen funcionar del todo bien

            while not(salir):
                if DEBUG:
                    print('Hijo  #', self._id_hijo, "\tEsperando al puerto GPIO", self._GPIOS[0][0], sep = '')

                if GPIO.event_detected(self._GPIOS[0][0]):                                                                          # Se comprueba el puerto que ha sido activado
                    if not(self._GPIOS[0][2]):                                                                                      # Si es una subida
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de subida esperado en el puerto GPIO", self._GPIOS[0][0], sep = '')

                        with semaforo:                                                                                              # Para realizar la conmutación es necesaria un semáforo o podría haber problemas
                            GPIO.output(self._GPIOS[1][0], not(GPIO.input(self._GPIOS[1][0])))                                      # Se conmuta la salida del puerto GPIO

                        if self._LLAMADAS[1] == True:                                                                               # Si se ha programado una llamada, ejecutar
                            self.cargar_y_ejecutar(self._LLAMADAS[0])

                        self._GPIOS[0][2] = not(self._GPIOS[0][2])                                                                  # Así se diferencia de las bajadas

                    elif self._GPIOS[0][2]:                                                                                         # Si es una bajada
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de bajada esperado en el puerto GPIO", self._GPIOS[0][0], sep = '')

                        if self._GPIOS[0][3] == self._config.SONDA:                                                                 # Si estamos ante una sonda, cada evento deberá conmutar siempre
                            with semaforo:                                                                                          # Para realizar la conmutación es necesaria un semáforo o podría haber problemas
                                GPIO.output(self._GPIOS[1][0], not(GPIO.input(self._GPIOS[1][0])))                                  # Se conmuta la salida del puerto GPIO

                        else:                                                                                                       # En caso contrario (botón), no es necesaria una acción
                            pass

                        if self._LLAMADAS[2] == True:                                                                               # Si se ha programado una llamada, ejecutar
                            self.cargar_y_ejecutar(self._LLAMADAS[0])

                        self._GPIOS[0][2] = not(self._GPIOS[0][2])                                                                  # Se prepara la próxima activación para una subida

                sleep(self._config.PAUSA)

            self.cerrar()

        except KeyboardInterrupt:
            self.cerrar()
            return


    def cargar_y_ejecutar(self, archivo):
        proceso = call('python3 ' + archivo, shell = True)

        if proceso == 0:
            return True

        else:
            return False


    def cerrar(self):
        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tDisparado el evento de cierre", sep = '')

        super().cerrar()


    def __del__(self):
        # super().__del__()                                                                                                         # La llamada al constructor de la clase padre está comentada a propósito
        pass


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = domotica_servidor(config, os.path.basename(sys.argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


def main_hijos(argv):
    app = domotica_servidor_hijos(argv, config)
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
