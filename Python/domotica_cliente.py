#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : domotica_cliente.py
# Description   : Parte cliente del sistema gestor de domótica
# Author        : Veltys
# Date          : 12-07-2018
# Version       : 1.1.7
# Usage         : python3 domotica_cliente.py [commandos]
# Notes         : Parte cliente del sistema en el que se gestionarán pares de puertos GPIO


DEBUG           = False
DEBUG_REMOTO    = False


import errno                                                                                    # Códigos de error
import socket                                                                                   # Tratamiento de sockets
import sys                                                                                      # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                               # Depuración remota

import comun                                                                                    # Funciones comunes a varios sistemas

try:
    from config import domotica_cliente_config as config                                        # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


class domotica_cliente(comun.app):
    ''' Clase del cliente del sistema gestor de domótica
    '''

    def __init__(self, config, argumentos):
        ''' Constructor de la clase:
            - Llama al constructor de la clase padre
            - Recoge los argumentos
            - Inicializa el socket
        '''

        super().__init__(config, False)

        self._argumentos = argumentos
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    def __comando(self):
        ''' Petición de comando:
            - Si aún hay argumentos, toma el siguiente como comando
            - Si no, lo pide al usuario
            - Lo normaliza y lo retorna
        '''

        if len(self._argumentos) == 1:
            comando = input('Introduzca un comando: ')

        else:
            comando = self._argumentos[1]
            self._argumentos.pop(1)

        comando = comando.lower()

        return comando


    def __describir(self, comando):
        ''' Descripción de puerto GPIO:
            - Si el estado de la conexión es el adecuado, solicita al servidor la descripción del puerto dado, la normaliza y la devuelve
            - Si no o en caso de fallo, devuelve una cadena vacía
        '''

        if self._estado_conexion >= comun.estados_conexion.LISTA_CARGADA:                       # Si el estado de la conexión es el adecuado
            mensaje = self._enviar_y_recibir(comando, True)                                     #     Se manda el comando y se recibe el mensaje

            if mensaje != False and mensaje[0:4] == 'info':                                     # Si se ha recibido un mensaje y es válido
                return mensaje[6:]                                                              #     Devolver la parte relevante del mensaje

            else:                                                                               # En caso contrario
                return ''                                                                       #     Devolver una cadena vacía

        else:                                                                                   # En caso contrario
            return ''                                                                           #     Devolver una cadena vacía


    def __estado(self, comando):
        ''' Estado de puerto GPIO:
            - Si el estado de la conexión es el adecuado, solicita al servidor el estado del puerto dado, la normaliza y la devuelve
            - Si no o en caso de fallo, devuelve una cadena vacía
        '''

        if self._estado_conexion >= comun.estados_conexion.LISTA_CARGADA:                       # Si el estado de la conexión es el adecuado
            mensaje = self._enviar_y_recibir(comando, True)                                     #     Se manda el comando y se recibe el mensaje

            if mensaje != False:                                                                #     Si se ha recibido un mensaje
                if mensaje[0:4] == 'info':                                                      #         Si el mensaje es válido
                    estado = int(mensaje[6:])                                                   #         Se preprocesa una parte

                    if estado == 0 or estado == 1:                                              #         Si la parte procesada está entre los valores correctos
                        return estado                                                           #             Se devuelve la parte preprocesada

                    else:                                                                       #         Si no
                        return -1                                                               #             Se devuelve -1

                else:                                                                           #         Si no
                    return -1                                                                   #             Se devuelve -1

            else:                                                                               #     Si no
                return -1                                                                       #         Se devuelve -1

        else:                                                                                   # Si no
            return -1                                                                           #     Se devuelve -1


    def __listar(self):
        ''' Listado de puertos GPIO:
            - Si el estado de la conexión es el adecuado:
                - Solicita al servidor la lista de puertos
                - la normaliza
                - la almacena en la variable de clase
                - Devuelve True
            - Si no o en caso de fallo:
                - Devuelve True
        '''

        if self._estado_conexion >= comun.estados_conexion.CONECTADO:                           # Si el estado de la conexión es el adecuado
            self._lista_GPIOS = self._enviar_y_recibir('listar')                                #     Se manda el comando y se almacena el mensaje

            if self._lista_GPIOS != False:                                                      #     Si se ha recibido un mensaje
                self._lista_GPIOS = self._lista_GPIOS[6:-1]                                     #         Éste es procesado
                self._lista_GPIOS = self._lista_GPIOS.split(' ')                                #         Y convertido en una lista

                if self._comprobar_lista_GPIOS():                                               #         Si es válido
                    self._estado_conexion = comun.estados_conexion.LISTA_CARGADA                #             El estado de la conexión es actualizado

                    for _, puerto in enumerate(self._lista_GPIOS):                              #             Se recorre la lista para transformarla en el formato necesario
                        puerto = (puerto, self.__estado('estado ' + aux), self.__describir('describir ' + aux))

                    self._estado_conexion = comun.estados_conexion.LISTA_EXTENDIDA              #             El estado de la conexión es actualizado de nuevo

                    return True                                                                 #             Se devuelve True

            else:                                                                               #     Si no
                print('Error: Sin lista de puertos GPIO, el servidor no responde', file = sys.stderr)
                print('Error: Imposible solicitar una lista de puertos GPIO, el servidor no responde')

                return False                                                                    #         Se devuelve False

        else:                                                                                   # Si no
            print('Error: Sin lista de puertos GPIO, estado de conexión inadecuado', file = sys.stderr)
            print('Error: Imposible solicitar una lista de puertos GPIO, no ' + self.estado_conexion_lenguaje_natural(self.estado_conexion() + 1))

            return False                                                                        # Se devuelve False


    def __mostrar_ayuda(self):
        ''' Muestra la ayuda de cada comando
        '''

        print('Comandos disponibles para la versión del protocolo ' , self._VERSION_PROTOCOLO  , ':', sep = '')

        if self._estado_conexion == 0    : print('Nota: después de conectar a un servidor, es posible que la lista de comandos se reduzca, si el protocolo a emplear es más antiguo respecto a la versión anteriormente citada')
        if self._VERSION_PROTOCOLO >= 1.0: print("\tconectar:\t\tConecta con el servidor")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tlistar:\t\t\tMuestra la lista de puertos GPIO disponibles")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tdesconectar:\t\tDesconecta del servidor")
        if self._VERSION_PROTOCOLO >= 1.1: print("\tdescribir <puerto>:\tMuestra el uso que el servidor le está dando al puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\testado <puerto>:\tMuestra el estado del puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tconmutar <puerto>:\tInvierte el estado del puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tencender <puerto>:\t\"Enciende\" el puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tapagar <puerto>:\t\"Apaga\" el puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tpulsar <puerto>:\t\"Pulsa\" (\"enciende\" y \"apaga\") el puerto GPIO especificado")
        if self._VERSION_PROTOCOLO >= 1.0: print("\tsalir:\t\t\tCierra la conexión (si hay alguna abierta) y termina la ejecución")


    def __mostrar_lista(self):
        ''' Muestra la lista de puertos GPIO almacenada:
            - Si el estado de la conexión es el adecuado:
                - Muestra dicha lista
                - Devuelve True
            - Si no:
                - Informa de ello
                - Devuelve false
        '''

        if self._estado_conexion >= comun.estados_conexion.LISTA_EXTENDIDA:                     # Si el estado de la conexión es el adecuado
            print('Ok: Puertos GPIO que están disponibles:')

            for puerto, estado, descipcion in self._lista_GPIOS:                                #     Recorre la lista de puertos, imprimiendo su información
                print("\t", 'Puerto GPIO', puerto, "\tEstado: ", ("activo\t" if estado == 1 else 'inactivo'), "\tDescripción: \"", descipcion, '"', sep = '')

            return True

        else:                                                                                   # Si no
            print('Error: Sin lista de puertos GPIO', file = sys.stderr)                        #     Informa de ello
            print('Error: No hay ninguna lista de puertos GPIO cargada')

            return False


    def __mostrar_estado(self, puerto, estado):
        ''' Muestra el estado de un puerto GPIO dado:
            - Si el estado de la conexión es el adecuado:
                - Si el estado de dicho puerto es válido
                    - Muestra el estado de dicho puerto
                    - Devuelve True
            - En caso de estado de conexión no adecuado o estado de puerto no válido:
                - Informa de ello
                - Devuelve False
        '''

        if self._estado_conexion >= comun.estados_conexion.LISTA_EXTENDIDA:                     # Si el estado de la conexión es el adecuado
            if int(estado) == 0 or int(estado) == 1:                                            #     Si el estado del puerto es válido, se informa del mismo
                print('Ok: Puerto GPIO' + puerto + ' --> Estado: ' + ('activo' if estado == 1 else 'inactivo'), sep = '')

                return True

            else:                                                                               #     Si no
                print('Error: Número de puerto GPIO no válido', file = sys.stderr)              #         Informa de ello
                print('Error: El número de puerto GPIO no es válido')

                return False

        else:                                                                                   # Si no
            print('Error: Sin lista de puertos GPIO', file = sys.stderr)                        #     Informa de ello
            print('Error: No hay ninguna lista de puertos GPIO cargada')

            return False


    def __varios(self, comando):
        ''' Método "comodín" para enviar y procesar la respuesta de los comandos apagar, conmutar, encender y pulsar
        '''

        if self._estado_conexion >= comun.estados_conexion.LISTA_CARGADA:                       # Si el estado de la conexión es el adecuado
            mensaje = self._enviar_y_recibir(comando)                                           #     Envía el comando y recibe el mensaje

            if mensaje == False:                                                                #     Si el envío del mensaje da error
                print('Error: Servidor no responde', file = sys.stderr)                         #         Se informa de ello
                print('Error: Imposible interaccionar con el puerto GPIO solicitado, el servidor no responde')

            elif mensaje[:2] == 'ok':                                                           #     Si el servidor devuelve un Ok, se informa de ello
                print('Ok: El servidor informa de que el comando "' + comando + '" ha sido ' + mensaje[4:], sep = '')

            elif mensaje[:4] == 'info' and (int(mensaje[5:]) == 0 or int(mensaje[5:]) == 1):    #     Si el servidor devuelve un Info, se informa de ello
                print('Ok: El servidor informa de que el estado del puerto "GPIO' + comando[7:] + '" es ' + mensaje[5:], sep = '')

            else:                                                                               #     Si el servidor devuelve otra respuesta, se informa de ello
                print('Aviso: El servidor informa de que el comando "' + comando + '" es ' + mensaje[5:], sep = '')

        else:                                                                                   # Si no, se informa de ello
            print('Error: Comando "' + comando + '" no ejecutado, estado de conexión inadecuado', file = sys.stderr)
            print('Error: El comando "' + comando + '" no ha sido ejecutado porque no' + self.estado_conexion_lenguaje_natural(self.estado_conexion() + 1), sep = '')


    def _comprobar_lista_GPIOS(self):
        ''' Método para la comprobación de la existencia de una lista de puertos GPIO
        '''

        try:                                                                                    # Bloque try
            self._lista_GPIOS                                                                   #     Intento de acceso

        except AttributeError:                                                                  #     Si no existe
            return False                                                                        #         Se devuelve False

        else:                                                                                   #     Si sí
            return True                                                                         #         Se devuelve True


    def bucle(self):
        ''' Realiza en bucle las tareas asignadas a este sistema
        '''

        try:
            comando = self.__comando()                                                          # Antes incluso de la ejecución en bucle, se pedirá un comando

            while comando != 'salir':                                                           # Mientras que el comando introducido no sea "salir" (condición de parada)
                if comando == 'ayuda':                                                          #     Si el comando es "ayuda"
                    self.__mostrar_ayuda()                                                      #         Se muestra la ayuda

                elif comando == 'conectar':                                                     #     Si el comando es "conectar" (implica "listar" y "estado" para cada puerto)
                    if self._conectar(True):                                                    #         Se procede a la conexión y se comprueba si ha tenido éxito
                        if self.__listar():                                                     #             Se procede al listado y se comprueba si ha tenido éxito
                            self.__mostrar_lista()                                              #                 Se muestra dicho listado


                #                                                                               #     Si el comando es "apagar", "conmutar", "encender" o "pulsar" y está bien formado
                elif (self._VERSION_PROTOCOLO >= 1.0 and comando != 'apagar'    and comando[0:6] == 'apagar'    and comando[6] == ' ' and comando[ 7:] != '') \
                  or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'conmutar'  and comando[0:8] == 'conmutar'  and comando[8] == ' ' and comando[ 9:] != '') \
                  or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'encender'  and comando[0:8] == 'encender'  and comando[8] == ' ' and comando[ 9:] != '') \
                  or (self._VERSION_PROTOCOLO >= 1.0 and comando != 'pulsar'    and comando[0:6] == 'pulsar'    and comando[6] == ' ' and comando[ 7:] != '') \
                :
                    self.__varios(comando)                                                      #         Se ejecuta

                #                                                                               #     Si el comando es "describir" y está bien formado
                elif  self._VERSION_PROTOCOLO >= 1.1 and comando != 'describir' and comando[0:9] == 'describir' and comando[9] == ' ' and comando[10:] != '':
                    self.__describir(comando)                                                   #         Se ejecuta

                elif comando == 'listar':                                                       #     Si el comando es "listar"
                    if self.__listar():                                                         #         Se procede al listado y si es válido
                        self.__mostrar_lista()                                                  #             Se muestra

                #                                                                               #     Si el comando es "estado" y está bien formado
                elif comando != 'estado' and comando[0:6] == 'estado' and comando[6] == ' ' and comando[7:] != '':
                    self.__mostrar_estado(comando[7:], self.__estado(comando))                  #         Se muestra el estado

                #                                                                               #     Si el comando es "apagar", "conmutar", "describir", "encender", "estado" o "pulsar" pero mal formado
                elif comando == 'apagar'    \
                  or comando == 'conmutar'  \
                  or comando == 'describir' \
                  or comando == 'encender'  \
                  or comando == 'estado'    \
                  or comando == 'pulsar'    \
                :
                    print('Error: Comando "' + comando + '" incorrecto', file = sys.stderr)     #         Se informa del error
                    print('Error: El comando "' + comando + '" requiere uno o más parámetros. Por favor, inténtelo de nuevo.')

                elif comando == 'desconectar':                                                  #     Si el comando es "desconectar"
                    self._desconectar()                                                         #         Se desconecta

                    print('Ok: Todas las conexiones abiertas han sido cerradas')                #         Y se informa de ello

                else:                                                                           #     Si es otro comando
                    print('Error: Comando "' + comando + '" no reconocido', file = sys.stderr)  #         Se informa de que es desconocido
                    print('Error: El comando "' + comando + '" no ha sido reconocido. Por favor, inténtelo de nuevo.')

                print()                                                                         # Llamar a print() sin argumentos introduce una nueva línea
                comando = self.__comando()

            if comando == 'salir':                                                              #     Si el comando es "salir" (la salida propiamente dicha será ejecutada en la siguiente vuelta del bucle)
                self.cerrar()                                                                   #         Se lleva a cabo el cierre

        except KeyboardInterrupt:
            self.cerrar()
            return


    def __del__(self):
        ''' Destructor de la clase:
            - Llama al Destructor de la clase padre
        '''

        super().__del__()


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    app = domotica_cliente(config, sys.argv)

    err = app.arranque()

    if err == 0:
        app.bucle()

    else:
        sys.exit(err)


if __name__ == '__main__':
    main(sys.argv)
