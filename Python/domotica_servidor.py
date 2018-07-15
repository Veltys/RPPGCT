#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_servidor.py
# Description   : Parte servidor del sistema gestor de domótica
# Author        : Veltys
# Date          : 13-07-2018
# Version       : 2.0.3
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


    def apagar(self, puerto, puerto_buscado = False):
        ''' Apaga el puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:                                                                                                                    # Si la id del puerto es válida
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], GPIO.LOW if self._config.GPIOS[puerto][3] else GPIO.HIGH)                        #         Se desactiva la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def bucle(self):
        ''' Realiza en bucle las tareas asignadas a este sistema
        '''

        try:
            if DEBUG:
                print('Padre #', os.getpid(), "\tMi configuración es: ", self._config.GPIOS, sep = '')
                print('Padre #', os.getpid(), "\tPienso iniciar ", int(len(self._config.GPIOS) / 2), ' hijos', sep = '')

            if not(DEBUG_PADRE):
                for i in range(int(len(self._config.GPIOS) / 2)):                                                                           #     Se recorre de dos en dos la lista de puertos GPIO para ir generando los hijos
                    if DEBUG:
                        print('Padre #', os.getpid(), "\tPreparando hijo ", i, sep = '')

                    self._hijos.append(Thread(target = main_hijos, args = (i,)))                                                            #         Se prepara cada hijo y se configura

                    if DEBUG:
                        print('Padre #', os.getpid(), "\tArrancando hijo ", i, sep = '')

                    self._hijos[i].start()                                                                                                  #         Se inicia cada hijo

            while True:                                                                                                                     # Se ejecutará siempre, ya que las condiciones de parada son externas
                sc, _ = self._socket.accept()                                                                                               #     Se espera hasta que haya un evento en el socket

                comando = sc.recv(1024)                                                                                                     #     Ante un evento, se recibe el contenido
                comando = comando.decode('utf_8')                                                                                           #     Se decodifica el mensaje recibido
                comando = comando.lower()                                                                                                   #     Y se normaliza

                if DEBUG:
                    print('Padre #', os.getpid(), "\tHe recibido el comando: ", comando, sep = '')

                while comando[0:11] != 'desconectar':                                                                                       #     Mientras que el comando recibido no sea el de desconexión
                    if comando == 'listar':                                                                                                 #         Si el comando es "listar"
                        mensaje = 'info: '                                                                                                  #             Se prepara el mensaje de respuesta

                        for i in range(0, int(len(self._config.GPIOS)), 2):                                                                 #             Se recorre la lista de puertos GPIO
                            mensaje = mensaje + str(self._config.GPIOS[i + 1][0]) + ' '                                                     #                 Y su información se añade al mensaje

                        if DEBUG:
                            print('Padre #', os.getpid(), "\tVoy a mandarle el mensaje: ", mensaje, sep = '')

                    #                                                                                                                       #         Si el comando es "apagar", "conmutar", "describir", "encender", "estado", "hola" o "pulsar" y está bien formado
                    elif (comando != 'apagar'       and comando[:6] == 'apagar'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (comando != 'conmutar'     and comando[:8] == 'conmutar'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (comando != 'describir'    and comando[:9] == 'describir'  and comando[9] == ' ' and comando[10:] != '') \
                      or (comando != 'encender'     and comando[:8] == 'encender'   and comando[8] == ' ' and comando[ 9:] != '') \
                      or (comando != 'estado'       and comando[:6] == 'estado'     and comando[6] == ' ' and comando[ 7:] != '') \
                      or (comando != 'hola'         and comando[:4] == 'hola'       and comando[4] == ' ' and comando[ 5:] != '') \
                      or (comando != 'pulsar'       and comando[:6] == 'pulsar'     and comando[6] == ' ' and comando[ 7:] != '') \
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

                            elif (comando[:6] == 'estado' and respuesta != -1) or (comando[0:9] == 'describir' and respuesta != False):
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


    def buscar_puerto_GPIO(self, puerto):
        ''' Convierte un número de puerto GPIO en una ID interna de la lista de puertos
            - Si el número de puerto dado está en la lista
                - Devuelve la ID de la lista
            - Si no
                - Devuelve -1
        '''

        res = -1                                                                                                                            # Precálculo del resultado fallido

        if isinstance(puerto, int) and puerto > 0 and puerto <= 27:                                                                         # Si el puerto es un entero, positivo y menor que 27 (27 es el número de puertos GPIO que tiene una Raspberry Pi)
            for i in range(1, len(self._config.GPIOS), 2):                                                                                  #     Se busca a lo largo de la lista de puertos
                if self._config.GPIOS[i][0] == puerto:                                                                                      #         Si hay una coincidencia con el número dado
                    res = i                                                                                                                 #             Se anotará la ID

                    break                                                                                                                   #             Y se detendrá la ejecución

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


    def conmutar(self, puerto, puerto_buscado = False):
        ''' Conmuta (invierte) el estado de un puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], not(GPIO.input(self._config.GPIOS[puerto][0])))                                  # Se conmuta la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def describir(self, puerto, puerto_buscado = False):
        ''' Devuelve la descripción de un puerto GPIO dado o False si hay algún error
        '''

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:                                                                                                                    # Si el puerto es correcto
            return self._config.GPIOS[puerto][4]                                                                                            #     Se devuelve su descripción

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def encender(self, puerto, puerto_buscado = False):
        ''' Enciende un puerto GPIO dado
        '''

        global semaforo                                                                                                                     # Es importante respetar la exclusión mutua

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:                                                                                                                    # Si el puerto es correcto
            with semaforo:                                                                                                                  #     Para realizar la operación es necesario un semáforo o podría haber problemas
                GPIO.output(self._config.GPIOS[puerto][0], GPIO.HIGH if self._config.GPIOS[puerto][3] else GPIO.LOW)                        #         Se activa la salida del puerto GPIO

            return True                                                                                                                     #     Se informa del éxito

        else:                                                                                                                               # Si no
            return False                                                                                                                    #     Se informa del fallo


    def estado(self, puerto, puerto_buscado = False):
        ''' Devuelve el estado de un puerto GPIO dado o -1 si hay algún error
        '''

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:                                                                                                                    # Si el puerto buscado ha sido hallado
            estado_puerto = GPIO.input(self._config.GPIOS[puerto][0])                                                                       #     Se recoge su estado

            return estado_puerto if self._config.GPIOS[puerto][3] else (estado_puerto + 1) % 2                                              #     Y se devuelve

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


    def pulsar(self, puerto, puerto_buscado = False):
        ''' Pulsa (enciende y apaga) un puerto GPIO dado
        '''

        if puerto_buscado == False:                                                                                                         # Si el puerto dado es un número de puerto y no una ID interna
            puerto = self.buscar_puerto_GPIO(puerto)                                                                                        #     Es necesario convertirlo a ID

        if puerto != -1:                                                                                                                    # Si el puerto es correcto
            res = self.encender(puerto, True)                                                                                               #     Condiciona el resultado a la devolución del método encender()

            sleep(2)

            res = res and self.apagar(puerto, True)                                                                                         #     Recondiciona el resultado anterior a la devolución del método apagar()

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

        self._GPIOS = []
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2])
        self._GPIOS.append(self._config.GPIOS[self._id_hijo * 2 + 1])

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
            GPIO.add_event_detect(self._GPIOS[0][0], GPIO.BOTH)                                                                             # Se añade el evento; se ha empleado GPIO.BOTH porque GPIO.RISING y GPIO.FALLING no parecen funcionar del todo bien

            while not(salir):                                                                                                               # Mientras la condición de parada no se active
                if DEBUG:
                    print('Hijo  #', self._id_hijo, "\tEsperando al puerto GPIO", self._GPIOS[0][0], sep = '')

                if GPIO.event_detected(self._GPIOS[0][0]):                                                                                  #     Se comprueba el puerto que ha sido activado
                    if not(self._GPIOS[0][3]):                                                                                              #         Si es una subida
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de subida esperado en el puerto GPIO", self._GPIOS[0][0], sep = '')

                        with semaforo:                                                                                                      #             Para realizar la operación es necesario un semáforo o podría haber problemas
                            GPIO.output(self._GPIOS[1][0], not(GPIO.input(self._GPIOS[1][0])))                                              #                 Se conmuta la salida del puerto GPIO

                        if self._LLAMADAS[1] == True:                                                                                       #             Si se ha programado una llamada
                            self.cargar_y_ejecutar(self._LLAMADAS[0])                                                                       #                 Se ejecuta

                        self._GPIOS[0][3] = not(self._GPIOS[0][3])                                                                          #             Así se diferencia de las bajadas

                    elif self._GPIOS[0][3]:                                                                                                 #         Si es una bajada
                        if DEBUG:
                            print('Hijo  #', self._id_hijo, "\tSe ha disparado el evento de bajada esperado en el puerto GPIO", self._GPIOS[0][0], sep = '')

                        if self._GPIOS[0][1] == self._config.SONDA:                                                                         #             Si se está ante una sonda, cada evento deberá conmutar siempre
                            with semaforo:                                                                                                  #                 Para realizar la operación es necesario un semáforo o podría haber problemas
                                GPIO.output(self._GPIOS[1][0], not(GPIO.input(self._GPIOS[1][0])))                                          #                     Se conmuta la salida del puerto GPIO

                        else:                                                                                                               #             En caso contrario (botón)
                            pass                                                                                                            #                 No es necesaria una acción

                        if self._LLAMADAS[3] == True:                                                                                       #             Si se ha programado una llamada
                            self._ejecutar(self._LLAMADAS[0])                                                                               #                 Ejecutar

                        self._GPIOS[0][3] = not(self._GPIOS[0][3])                                                                          #             Se prepara la próxima activación para una subida

                sleep(self._config.PAUSA)                                                                                                   #     Pausa programada para evitar la saturación del sistema

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
        proceso = call('python3 ' + os.path.dirname(os.path.abspath(__file__)) + '/' + archivo, shell = True)

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
