#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : config.py
# Description   : Módulo configurador para ser importado en el resto de módulos o sistemas que lo necesiten
# Author        : Veltys
# Date          : 24-05-2018
# Version       : 1.7.0
# Usage         : import config | from config import <clase>
# Notes         : A título ilustrativo, a se ofrece una configuración por defecto (la mía, para ser exactos)


import os                                                                                   # Funcionalidades varias del sistema operativo

from time import strftime                                                                   # Formato de fecha y hora


class config_global(object):                                                                # Configuración común
    IP_DEP_REMOTA   = '0.0.0.0'                                                             # IP del servidor de depuración

    RELE            = 0
    LED             = 0
    BOTON           = 1
    SONDA           = 2


class aviso_electricidad_config(config_global):
    ASUNTO          = '<NOMBRE_SISTEMA>: informe especial'
    CONTRASENYA     = ''
    CORREO          = 'Informe especial de <NOMBRE_SISTEMA>, generado el ' + str(strftime("%c")) + os.linesep + os.linesep \
                    + 'Ha habido un corte de luz en la red eléctrica de <NOMBRE_SISTEMA> y se ha activado la batería.'
    DE              = ''
    PARA            = ''
    SERVIDOR        = ''
    USUARIO         = ''


class cpu_config(config_global):                                                            # Configuración del sistema de CPU
    GPIOS           = [(26, True,  True , config_global.LED  , 'Verde'                   ), # GPIOS contiene quíntuplas de datos en formato lista:
                       (19, True,  True , config_global.LED  , 'Amarillo'                ), # el primer elemento será el número (BCM) de puerto GPIO a manipular,
                       (13, True,  True , config_global.LED  , 'Naranja'                 ), # el segundo, el modo (True para salida, False para entrada)
                       ( 6, True,  True , config_global.LED  , 'Rojo'                    ), # el tercero, la activación si es de salida (True si es activo a alto nivel o False si es a bajo nivel) o el estado si es de entrada (True si está bajado y False subido)
                       ( 5, True,  True , config_global.LED  , 'Alarma'                  ), # el cuarto, el tipo de elemento que es
                      ]                                                                     # y el quinto, una muy breve descripción de su función

    PAUSA           = 10                                                                    # PAUSA contiene el tiempo que el bucle estará parado

    senyales        = {'SIGTERM': 'sig_cerrar',                                             # senyales (señales) contiene el tipo de señal y la función a la que ésta se asociará
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }


class dht11_config(config_global):
    GPIOS           = [(25, False, False, config_global.SONDA, 'Sonda DHT11 de pruebas'  ),
                      ]

    LIMITE          = 20

    PAUSA           = 0.5


class domotica_cliente_config(config_global):
    puerto          = 4710                                                                  # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
                                                                                            # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85


class domotica_servidor_config(domotica_cliente_config):
    GPIOS           = [(22, False, False, config_global.BOTON, 'Botón reinicio router'   ), # En este caso, los puertos GPIO serán dados por pares:
                       ( 4, True,  False, config_global.RELE , 'Relé reinicio router'    ), # Las entradas impares corresponderán a los relés que se gestionarán

                       (24, False, False, config_global.BOTON, 'Botón reinicio switch'   ), # Las pares, a los pulsadores o equivalentes que irán asociados a dichos relés, para su conmutación
                       (23, True,  False, config_global.RELE , 'Relé reinicio switch'    ),

                       (17, False, False, config_global.BOTON, 'Botón reinicio cámara'   ),
                       (27, True,  False, config_global.RELE , 'Relé reinicio cámara'    ),

                       (13, False, False, config_global.SONDA, 'Indicador electricidad'  ),
                       (16, True,  False, config_global.RELE , 'Relé activación router'  ),
                      ]

    LLAMADAS        = [# (None,                    False, False),
                       # (None,                    False, False),
                       # (None,                    False, False),
                       ('aviso_electricidad.py', False, True ),
                      ]

    PAUSA           = 0.20

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class internet_config(config_global):
    HOSTS           = ['google.es',                                                         # HOSTS contiene los servidores a los cuales se les hará ping para comprobar si hay internet
                       '2001:4860:4860::8888',
                       '2001:4860:4860::8844',
                       '8.8.8.8',
                       '8.8.4.4',
                       'opendns.com',
                       '2620:0:ccc::2',
                       '2620:0:ccd::2',
                       '208.67.222.222',
                       '208.67.220.220',
                      ]


class reiniciar_router_config(domotica_cliente_config):
    PAUSA           = 15

    GPIO            = [domotica_servidor_config.GPIOS[1],
                       domotica_servidor_config.GPIOS[3],
                      ]

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class temperatura_config(config_global):
    COLORES         = [(0.0, 0.0, 1.0, 0.0),                                                # COLORES contiene una matriz de 4 x 4 que, por columnas, representa cada led y, por filas, la etapa de temperatura
                       (0.0, 1.0, 0.0, 0.0),
                       (1.0, 0.6, 0.0, 0.0),
                       (1.0, 0.0, 0.0, 1.0),
                      ]

    FRECUENCIA      = 60                                                                    # FRECUENCIA contiene la frecuencia (en herzios) de refresco de los leds

    GPIOS           = [(16, True,  True , config_global.LED  , 'Frío'                    ),
                       (20, True,  True , config_global.LED  , 'Intermedio'              ),
                       (21, True,  True , config_global.LED  , 'Caliente'                ),
                       (12, True,  True , config_global.LED  , 'Alarma'                  ),
                      ]

    TEMPERATURAS    = [40, 45, 50]                                                          # TEMPERATURAS contiene las temperaturas de activación de cada etapa

    PAUSA           = 60

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }
