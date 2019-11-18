#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : config.py
# Description   : Módulo configurador para ser importado en el resto de módulos o sistemas que lo necesiten
# Author        : Veltys
# Date          : 30-06-2019
# Version       : 1.10.0
# Usage         : import config | from config import <clase>
# Notes         : A título ilustrativo, a se ofrece una configuración por defecto (la mía, para ser exactos)


import os                                                                                                   # Funcionalidades varias del sistema operativo

from time import strftime                                                                                   # Formato de fecha y hora


class config_global(object):                                                                                # Configuración común
    IP_DEP_REMOTA       = '255.255.255.255'                                                                 # IP del servidor de depuración

    RELE                = 0
    LED                 = 10
    LED_PWM             = 11
    BOTON               = 20
    SONDA               = 30


class aviso_electricidad_config(config_global):                                                             # Configuración del sistema de aviso en caso de corte de electricidad
    ASUNTO              = '<NOMBRE_SISTEMA>: informe especial'
    CORREO              = 'Informe especial de <NOMBRE_SISTEMA>, generado el ' + str(strftime("%c")) + os.linesep + os.linesep \
                        + 'Ha habido un corte en la red eléctrica de <NOMBRE_SISTEMA> y se ha activado la batería.'
    DE                  = ''
    PARA                = ''
    PAUSA               = 10
    REINTENTOS          = 10


class correo_electronico_config(config_global):                                                             # Configuración del sistema de correo electrónico
    CONTRASENYA         = ''
    SERVIDOR            = ''
    USUARIO             = ''


class cpu_config(config_global):                                                                            # Configuración del sistema de CPU
    GPIOS               = [
                            (26, config_global.LED      , None, True , 'Verde'                      ),      # GPIOS contiene quíntuplas de datos en formato lista:
                            (19, config_global.LED      , None, True , 'Amarillo'                   ),      # el primer elemento será el número (BCM) de puerto GPIO a manipular,
                            (13, config_global.LED      , None, True , 'Naranja'                    ),      # el segundo, el tipo de elemento que es
                            ( 6, config_global.LED      , None, True , 'Rojo'                       ),      # el tercero, un "placeholder" que, en el caso de ser un puerto controlado por PWM, contendrá el objeto de control del elemento
                            ( 5, config_global.LED      , None, True , 'Alarma'                     ),      # el cuarto, la activación si es de salida (True si es activo a alto nivel o False si es a bajo nivel) o el estado si es de entrada (True si está bajado y False subido)
                          ]                                                                                 # y el quinto, una muy breve descripción de su función

    PAUSA               = 10                                                                                # PAUSA contiene el tiempo que el bucle estará parado

    senyales            = {                                                                                 # senyales (señales) contiene el tipo de señal y la función a la que ésta se asociará
                            'SIGTERM': 'sig_cerrar',
                            'SIGUSR1': 'sig_test',
                            'SIGUSR2': 'sig_apagado',
                          }


class dht11_config(config_global):                                                                          # Configuración del sistema de sondas DHT11
    GPIOS               = [
                            (25, config_global.SONDA    , None, False, 'Sonda DHT11 de pruebas'     ),
                          ]

    LIMITE              = 20

    PAUSA               = 0.5


class domotica_cliente_config(config_global):                                                               # Configuración del sistema cliente de domótica
    puerto              = 4710                                                                              # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
    #                                                                                                       # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85


class domotica_servidor_config(domotica_cliente_config):                                                    # Configuración del sistema servidor de domótica
    GPIOS               = [                                                                                 # En este caso, los puertos GPIO serán anidados:
                            (                                                                               # Las entradas en la misma tupla estarán vinculadas entre sí y se gestionarán como un todo. Por ejemplo:
                                (22, config_global.BOTON    , None, False, 'Botón reinicio router'      ),  # Un botón de activación...
                                ( 4, config_global.RELE     , None, False, 'Relé reinicio router'       ),  # ... y su correspondiente relé
                            ),
    
                            (
                                (24, config_global.BOTON    , None, False, 'Botón reinicio switch'      ),  # Las pares, a los pulsadores o equivalentes que irán asociados a dichos relés, para su conmutación
                                (23, config_global.RELE     , None, False, 'Relé reinicio switch'       ),
                            ),
    
                            (
                                (17, config_global.BOTON    , None, False, 'Botón reinicio cámara'      ),
                                (27, config_global.RELE     , None, False, 'Relé reinicio cámara'       ),
                            ),

                            (
                                (14, config_global.SONDA    , None, False, 'Indicador electricidad'     ),
                                (15, config_global.RELE     , None, False, 'Relé activación router'     ),
                            ),
                          ]

    LLAMADAS            = [                                                                                 # LLAMADAS determina, qué debe ser llamado por cada hijo y cuándo
                            (None                   , False, False),                                        # El primer elemento de cada tupla es el comando (en python, por seguridad) a llamar
                            (None                   , False, False),                                        # El segundo, si debe ser llamado cuando se dispare un evento de bajada
                            (None                   , False, False),                                        # Y el tercero, si debe ser llamado cuando se dispare un evento de subida
                            ('aviso_electricidad.py', False, True ),
                          ]

    PAUSA               = 0.20

    TIEMPO_PULSACION    = 2

    senyales            = {
                            'SIGTERM': 'sig_cerrar',
                            'SIGUSR1': 'sig_test'  ,
                          }


class internet_config(config_global):                                                                       # Configuración del sistema de comprobación de conectividad a Internet
    HOSTS               = [                                                                                 # HOSTS contiene los servidores a los cuales se les hará ping para comprobar si hay internet
                            'google.es'                ,
                            '2001:4860:4860::8888'     ,
                            '2001:4860:4860::8844'     ,
                            '8.8.8.8'                  ,
                            '8.8.4.4'                  ,
                            'opendns.com'              ,
                            '2620:0:ccc::2'            ,
                            '2620:0:ccd::2'            ,
                            '208.67.222.222'           ,
                            '208.67.220.220'           ,
                          ]


class reiniciar_router_config(domotica_cliente_config):                                                     # Configuración del sistema de reinicio de router en caso de pérdida de conectividad
    PAUSA               = 15

    PUERTOS             = [
                            domotica_servidor_config.GPIOS[0][1][0],
                            domotica_servidor_config.GPIOS[1][1][0],
                          ]

    senyales            = {
                            'SIGTERM': 'sig_cerrar',
                            'SIGUSR1': 'sig_test'  ,
                          }


class temperatura_config(config_global):                                                                    # Configuración del sistema de temperaturas
    COLORES             = [                                                                                 # COLORES contiene una matriz de 4 x 4 que, por columnas, representa cada led y, por filas, la etapa de temperatura
                            (0.0, 1.0, 0.0, 0.0),
                            (1.0, 0.6, 0.0, 0.0),
                            (1.0, 0.0, 0.0, 0.0),
                            (1.0, 0.0, 0.0, 1.0),
                          ]

    FRECUENCIA          = 60                                                                                # FRECUENCIA contiene la frecuencia (en herzios) de refresco de los leds

    GPIOS               = [
                            (12, config_global.LED_PWM  , None, True , 'Rojo'                       ),
                            (16, config_global.LED_PWM  , None, True , 'Verde'                      ),
                            (20, config_global.LED_PWM  , None, True , 'Azul'                       ),
                            (26, config_global.LED_PWM  , None, True , 'Alarma'                     ),
                          ]

    PAUSA               = 60

    RELES               = [
                            domotica_servidor_config.GPIOS[4][0],
                            domotica_servidor_config.GPIOS[5][0],
                          ]

    TEMPERATURAS        = [40, 50, 60]                                                                      # TEMPERATURAS contiene las temperaturas de activación de cada etapa

    senyales            = {
                            'SIGTERM': 'sig_cerrar' ,
                            'SIGUSR1': 'sig_test'   ,
                            'SIGUSR2': 'sig_apagado',
                          }


