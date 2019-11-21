#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_servidor.py
# Description   : Parte servidor del sistema gestor de domótica
# Author        : Veltys
# Date          : 18-11-2019
# Version       : 2.2.0
# Usage         : python3 domotica_servidor.py
# Notes         : Parte servidor del sistema en el que se gestionarán pares de puertos GPIO
#                 Las entradas impares en la variable de configuración asociada GPIOS corresponderán a los relés que se gestionarán
#                 Las pares, a los pulsadores que irán asociados a dichos relés, para su conmutación
#                 Se está estudiando, para futuras versiones, la integración con servicios IoT, especuialmente con el "AWS IoT Button" --> http://amzn.eu/dsgsHvv


DEBUG           = False
DEBUG_PADRE     = False
DEBUG_REMOTO    = False


salir           = False                                                                                                                     # Ya que no es posible matar a un hilo, esta "bandera" global servirá para indicarle a los hilos que deben terminar


import errno                                                                                                                                # Códigos de error
import os                                                                                                                                   # Funcionalidades varias del sistema operativo
import sys                                                                                                                                  # Funcionalidades varias del sistema
import socket                                                                                                                               # Tratamiento de sockets

if DEBUG_REMOTO:
    import pydevd                                                                                                                           # Depuración remota

import RPi.GPIO as GPIO                                                                                                                     # Acceso a los pines GPIO

import comun                                                                                                                                # Funciones comunes a varios sistemas

from subprocess import call                                                                                                                 # Lanzamiento de nuevos procesos
from threading import Lock, Thread                                                                                                          # Capacidades multihilo
from time import sleep                                                                                                                      # Para hacer pausas

if DEBUG_REMOTO:
    from pydevd_file_utils import setup_client_server_paths                                                                                 # Configuración de las rutas Eclipse ➡

try:
    from config import domotica_servidor_config as config                                                                                   # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


semaforo        = Lock()                                                                                                                    # Un semáforo evitará que el padre y los hijos den problemas al acceder a una variable que ambos puedan modificar


class domotica_servidor(comun.app):
    ''' Clase del servidor del sistema gestor de domótica
    '''

    def __init__(self, config, nombre):
        ''' Constructor de la clase:
            - Llama al constructor de la clase padre
            - Inicializa el socket
            - Se pone a la escucha
        '''

        self._hijos = []                                                                                                                    # Preparación de la lista contenedora de hijos

        super().__init__(config, nombre)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:                                                                                                                                # Bloque try
            self._socket.bind(('127.0.0.1', self._config.puerto))

            # self._socket.bind(('::1', self._config.puerto))                                                                               #     TODO: IPv6

        except OSError:                                                                                                                     # Error del sistema operativo
            self.cerrar()

            print('Error: Puerto', self._config.puerto, 'en uso', file = sys.stderr)
            print('Error: Imposible abrir un socket en el puerto', self._config.puerto, ', el puerto ya está en uso')

            sys.exit(errno.EADDRINUSE)                                                                                                      #     Salida del sistema

        else:
            self._socket.listen(1)                                                                                                          #     FIXME: No se preveen muchas conexiones, así que, por ahora, se soportará solamente un cliente


    def apagar(self, gpio, buscar = True):
        ''' Apaga el puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si la id del puerto es válida
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(gpio[0], GPIO.LOW if gpio[3] else GPIO.HIGH)                                                                    #         Se desactiva la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def bucle(self):
        ''' Realiza en bucle las tareas asignadas a este sistema
        '''

        try:
            if DEBUG:
                print('Padre #', os.getpid(), "\tMi configuración es: ", self._config.GPIOS, sep = '')
                print('Padre #', os.getpid(), "\tPienso iniciarun máximo de ", int(len(self._config.GPIOS)), ' hijos', sep = '')            #     Ya no es posible saber a priori cuántos hijos serán inciados

            if not(DEBUG_PADRE):
                i = 0                                                                                                                       #     Contador para generar las IDs de los hijos

                for puertos in self._config.GPIOS:                                                                                          #     Se recorre la lista de puertos GPIO para ir generando los hijos
                    for _, tipo, _, _, _ in puertos:
                        generar_hijo = False

                        if tipo == self._config.BOTON or tipo == self._config.SONDA:                                                        #         Si el elemento es de tipo botón o superior (sonda)
                            generar_hijo = True                                                                                             #             Se generará un hijo

                        if generar_hijo:                                                                                                    #         Si es necesario generar un hijo
                            if DEBUG:
                                print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

                            self._hijos.append(Thread(target = main_hijos, args = (i,)))                                                    #             Se prepara hijo, se configura...

                            if DEBUG:
                                print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

                            self._hijos[-1].start()                                                                                         #             ... y se inicia

                            i = i + 1                                                                                                       #             Se incrementa el contador para cada hijo generado

            while True:                                                                                                                     # Se ejecutará siempre, ya que las condiciones de parada son externas
                sc, _ = self._socket.accept()                                                                                               #     Se espera hasta que haya un evento en el socket

                comando = sc.recv(1024)                                                                                                     #     Ante un evento, se recibe el contenido
                comando = comando.decode('utf_8')                                                                                           #     Se decodifica el mensaje recibido
                comando = comando.lower()                                                                                                   #     Y se normaliza

                if DEBUG:
                    print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

                while comando[0:11] != 'desconectar':                                                                                       #     Mientras que el comando recibido no sea el de desconexión
                    if self._VERSION_PROTOCOLO >= 1.0 and comando == 'listar':                                                              #         Si el comando es "listar"
                        mensaje = 'info: '                                                                                                  #             Se prepara el mensaje de respuesta

                        for puertos in self._config.GPIOS:                                                                                  #             Se recorre la lista de puertos GPIO
                            for gpio, tipo, _, _, _ in puertos:
                                if tipo == config.RELE:
                                    mensaje = mensaje + str(gpio) + ' '                                              #                 Y su información se añade al mensaje

                        if DEBUG:
                            print('Padre #', os.getpid(), "\tVoy a mandarle el mensaje: ", mensaje, sep = '')

                    #                                                                                                                       #         Si el comando es "apagar", "conmutar", "describir", "encender", "estado", "hola" o "pulsar" y está bien formado
                    elif (self._VERSION_PROTOCOLO >= 1.0 and comando != 'apagar'       and comando[:6] == 'apagar'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'conmutar'     and comando[:8] == 'conmutar'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.1 and comando != 'describir'    and comando[:9] == 'describir'  and comando[9] == ' ' and comando[10:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'encender'     and comando[:8] == 'encender'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'estado'       and comando[:6] == 'estado'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'hola'         and comando[:4] == 'hola'       and comando[4] == ' ' and comando[ 5:] != '') \
                      or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'pulsar'       and comando[:6] == 'pulsar'     and comando[6] == ' ' and comando[ 7:] != '') \
                    :
                        funcion, params = comando.split(' ', 1)                                                                             #             Se prepara su ejecución

                        try:                                                                                                                #             Bloque try
                            respuesta = eval('self.' + funcion + '(' + params + ')')                                                        #                 Se ejecuta y anexa al mensaje de respuesta el retorno del método

                        except AttributeError:                                                                                              #             Error de comando no implementado
                            if DEBUG:
                                print('Padre #', os.getpid(), "\tEl comando \"" + comando + '" es incorrecto o no está implementado', sep = '')

                            mensaje = 'err: incorrecto o no implementado'                                                                   #                 Se establece la respuesta

                        else:                                                                                                               #             Si todo ha ido bien, se establece la respuesta en función del comando recibido
                            if comando[:4] == 'hola':
                                mensaje = respuesta

                            elif comando[:6] != 'estado' and comando[:9] != 'describir' and respuesta:
                                mensaje = 'ok: ejecutado'

                            elif (comando[:6] == 'estado' and respuesta != -1) or (comando[0:9] == 'describir' and respuesta):
                                mensaje = 'info: ' + str(respuesta)

                            else:
                                mensaje = 'err: no ejecutado, puerto incorrecto o no encontrado'

                    else:                                                                                                                   #         Si el comando es desconocido
                        mensaje = 'err: no ejecutado, comando incorrecto'                                                                   #             Se establece la respuesta

                    try:                                                                                                                    #             Bloque try
                        sc.send(mensaje.encode('utf_8'))                                                                                    #                 Se manda el mensaje

                    except BrokenPipeError:                                                                                                 #             Error de tubería rota
                        comando = 'desconectar'                                                                                             #                 Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

                    except ConnectionResetError:                                                                                            #             Error de conexión reiniciada
                        comando = 'desconectar'                                                                                             #                 Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

                    except OSError:                                                                                                         #             Error del sistema operativo
                        comando = 'desconectar'                                                                                             #                 Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

                    else:                                                                                                                   #             Si todo ha ido bien (nótese la duplicidad de código; ¡gracias, Python, por no implementar la estructura do - while!)
                        try:                                                                                                                #             Bloque try
                            comando = sc.recv(1024)                                                                                         #                 Ante un evento, se recibe el contenido

                        except ConnectionResetError:                                                                                        #             Error de conexión reiniciada
                            comando = 'desconectar'                                                                                         #                 Se precarga el comando de desconexión para que sea ejecutado en la siguiente vuelta

                        else:                                                                                                               #             Si todo ha ido bien
                            comando = comando.decode('utf_8')                                                                               #                 Se decodifica el mensaje recibido
                            comando = comando.lower()                                                                                       #                 Y se normaliza

                    finally:                                                                                                                #             En cualquier caso
                        if DEBUG:
                            print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

                # else:                                                                                                                     #     Cuando el comando sea "desconectar"
                sc.close()                                                                                                                  #         Se cerrará el socket y vuelta a empezar

        except KeyboardInterrupt:
            self.cerrar()
            return


    def buscar_gpio(self, gpio):
        ''' Devuelve, a partir de un número de puerto GPIO, la tupla de control correspondiente
            - Si el número de puerto dado está en la lista
                - Devuelve la tupla de control correspondiente
            - Si no
                - Devuelve False
        '''

        res = False                                                                                                                            # Precálculo del resultado fallido

        if isinstance(gpio, int) and gpio > 0 and gpio <= 27:                                                                               # Si el puerto GPIO es un entero, positivo y menor que 27 (27 es el número de puertos GPIO que tiene una Raspberry Pi)
            for i in range(len(self._config.GPIOS)):                                                                                        #     Se busca a lo largo de la lista de puertos
                for j in range(len(self._config.GPIOS[i])):
                    if self._config.GPIOS[i][j][0] == gpio:                                                                                 #         Si hay una coincidencia con el número dado
                        res = self._config.GPIOS[i][j]                                                                                      #             Se recupera la entrada correspondiente

                        break                                                                                                               #             Y se saldrá del bucle

        return res                                                                                                                          # Se retorna el resultado


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema
        '''

        global salir                                                                                                                        # Es necesario indicar que estamos ante una variable global, ya que, de lo contrario, se estaría trabajando con una variable homónima de ámbito local al método

        salir = True                                                                                                                        # Se establece la condición de para global para los hijos

        if DEBUG:
            print('Padre #', os.getpid(), "\tDisparado el evento de cierre", sep = '')

        if not(DEBUG_PADRE):
            for hijo in self._hijos:                                                                                                        # Una vez establecida, se recorren los hijos
                hijo.join()                                                                                                                 #     Para esperar su finalización

        super().cerrar()                                                                                                                    # Llamada al método cerrar() del padre también


    def conmutar(self, gpio, buscar = True):
        ''' Conmuta (invierte) el estado de un puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si el puerto es correcto
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(gpio[0], not(gpio[0]))                                                                                          #         Se conmuta la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def describir(self, gpio, buscar = True):
        ''' Devuelve la descripción de un puerto GPIO dado o False si hay algún error
        '''

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si el puerto es correcto
            return gpio[4]                                                                                                                  #     Se devuelve su descripción

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def encender(self, gpio, buscar = True):
        ''' Enciende un puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si el puerto es correcto
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(gpio[0], GPIO.HIGH if gpio[3] else GPIO.LOW)                                                                    #         Se activa la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def estado(self, gpio, buscar = True):
        ''' Devuelve el estado de un puerto GPIO dado o -1 si hay algún error
        '''

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si el puerto buscado ha sido hallado
            estado_puerto = GPIO.input(gpio[0])                                                                                             #     Se recoge su estado

            return estado_puerto if gpio[3] else (estado_puerto + 1) % 2                                                                    #     Y se devuelve

        else:                                                                                                                               # Si no
            return -1                                                                                                                       #     Se informa del fallo


    def hola(self, version):
        ''' Evalúa el protocolo que el servidor, lo compara con el que el cliente maneja maneja y responde en consecuencia
        '''

        test = self._VERSION_PROTOCOLO - float(version)                                                                                     # Se evalúan ambas versiones (la del servidor y la del cliente) como una resta de "floats"

        if test < 0:                                                                                                                        # Si la versión del servidor es superior...
            self._VERSION_PROTOCOLO = float(version)                                                                                        # ... se adapta...

            return 'Ok: ' + str(version)                                                                                                    # ... y se responde "Ok"

        elif test == 0:                                                                                                                     # Si la versión del servidor es la misma...
            return 'Ok: ' + str(version)                                                                                                    # ... se responde "Ok"

        else:                                                                                                                               # Si la versión del servidor es inferior...
            return 'Info: ' + str(self._VERSION_PROTOCOLO)                                                                                  # ... se pide al cliente que se adapte


    def pulsar(self, gpio, buscar = True):
        ''' Pulsa (enciende y apaga) un puerto GPIO dado
        '''

        if buscar:                                                                                                                          # Si es necesario buscar el puerto GPIO dado para recuperar sus características
            gpio = self.buscar_gpio(gpio)                                                                                                   #     Se busca y se obtiene el elemento

        if gpio:                                                                                                                            # Si el puerto es correcto
            res = self.encender(gpio, False)                                                                                                #     Condiciona el resultado a la devolución del método encender()

            sleep(self._config.PULSACION)

            res = res and self.apagar(gpio, False)                                                                                          #     Recondiciona el resultado anterior a la devolución del método apagar()

        else:                                                                                                                               # Si no
            res = False                                                                                                                     #     Establece el resultado como erróneo

        return res                                                                                                                          # Devuelve el resultado


    def __del__(self):
        ''' Destructor de la clase:
            - Llama al Destructor de la clase padre
        '''

        super().__del__()


class domotica_servidor_hijos(comun.app):
    ''' Clase de los hijos del servidor del sistema gestor de domótica
    '''

    def __init__(self, id_hijo, config):
        ''' Constructor de la clase:
            - Inicializa variables
            - Carga la configuración
        '''

        # super().__init__()                                                                                                                # La llamada al constructor de la clase padre está desactivada a propósito

        self._config = config
        self._bloqueo = False
        self._estado_conexion = comun.estados_conexion.DESCONECTADO
        self._modo_apagado = False

        self._id_hijo = id_hijo

        self._GPIOS = self._config.GPIOS[self._id_hijo]

        self._LLAMADAS = self._config.LLAMADAS[self._id_hijo]

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tMi configuración es ", self._GPIOS, sep = '')
            print('Hijo  #', self._id_hijo, "\tDeberé escuchar en el puerto GPIO", self._GPIOS[0][0] , ' y conmutar el puerto GPIO', self._GPIOS[1][0], sep = '')


    def arranque(self):
        ''' Lleva a cabo las tareas necesarias para el "arranque" de la aplicación
        '''

        # super().arranque()                                                                                                                # La llamada al método de la clase padre está desactivada a propósito

        return 0                                                                                                                            # En este caso, no es necesario realizar operaciones de arranque, ya que el hilo padre las ha realizado todas, por lo cual se devuelve 0, que significa que todo se ha realizado correctamente


    def bucle(self):
        ''' Realiza en bucle las tareas asignadas a este sistema
        '''

        global salir, semaforo

        try:
            for gpio, tipo, _, _, _ in self._GPIOS:
                if tipo == self._config.BOTON or tipo == self._config.SONDA:
                    GPIO.add_event_detect(gpio, GPIO.BOTH)                                                                                  # Se añade el evento; se ha empleado GPIO.BOTH porque GPIO.RISING y GPIO.FALLING no parecen funcionar del todo bien

            while not(salir):                                                                                                               # Mientras la condición de parada no se active
                activado = 0                                                                                                                #     Variable de activado: 0 ➡ no activado; 1 ➡ activado de subida; 2 ➡ activado de bajada

                for gpio, tipo, _, activacion, _ in self._GPIOS:
                    if tipo == self._config.BOTON or tipo == self._config.SONDA:                                                            #         Si se está ante un elemento de entrada
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tEsperando al puerto GPIO", gpio, sep = '')

                        if GPIO.event_detected(gpio):                                                                                       #             Se comprueba el puerto que ha sido activado
                            if not(activacion):                                                                                             #                 Si es una subida
                                if DEBUG:
                                    print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de subida esperado en el puerto GPIO", gpio, sep = '')

                                activado = 1                                                                                                #                     Se programa la ejecución posterior

                            else: # elif activacion:                                                                                        #                 Si es una bajada
                                if DEBUG:
                                    print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de bajada esperado en el puerto GPIO", gpio, sep = '')

                                activado = 2                                                                                                #                     Se programa la ejecución posterior

                            activacion = not(activacion)                                                                                    #                 Se prepara la próxima activación

                    elif tipo == self._config.RELE:                                                                                         #         Si se está ante un elemento de salida
                        if activado > 0:                                                                                                    #             Si ha sido activado
                            with semaforo:                                                                                                  #                 Para realizar la operación es necesario un semáforo o podría haber problemas
                                GPIO.output(gpio, not(GPIO.input(gpio)))                                                                    #                     Se conmuta la salida del puerto GPIO

                if activado > 0:                                                                                                            #         Una vez recorrida la tupla, se vuelve a comprobar si ha sido activado
                    if self._LLAMADAS[1]:                                                                                                   #             Si se ha programado una llamada
                        self.cargar_y_ejecutar(self._LLAMADAS[0])                                                                           #                 Se ejecuta

                sleep(self._config.PAUSA)                                                                                                   #         Pausa programada para evitar la saturación del sistema

            self.cerrar()                                                                                                                   # Cuando se salga del bucle, se ejecutarán las rutinas de salida

        except KeyboardInterrupt:
            self.cerrar()

            return


    def cerrar(self):
        ''' Realiza las operaciones necesarias para el cierre del sistema
        '''

        if DEBUG:
            print('Hijo  #', self._id_hijo, "\tDisparado el evento de cierre", sep = '')

        # super().cerrar()                                                                                                                  # La llamada al método de cierre de la clase padre está desactivada a propósito


    @staticmethod                                                                                                                           # Método estático
    def _ejecutar(archivo):
        ''' Ejecuta un script en python3 dado
        '''

        proceso = call(sys.executable + os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, shell = True)

        if proceso == 0:                                                                                                                    # Si el proceso devolvió una ejecución correcta
            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def __del__(self):
        ''' Destructor de la clase:
            - No es necesario que haga nada
        '''

        # super().__del__()                                                                                                                 # La llamada al constructor de la clase padre está desactivada a propósito

        pass


def main(argv):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA, trace_only_current_thread = False)

    app = domotica_servidor(config, os.path.basename(sys.argv[0]))
    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


def main_hijos(argv):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA, trace_only_current_thread = False)

    app = domotica_servidor_hijos(argv, config)

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
