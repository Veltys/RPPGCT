#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : config.py
# Description   : Módulo configurador para ser importado en el resto de módulos o sistemas que lo necesiten
# Author        : Veltys
# Date          : 10-08-2017
# Version       : 1.3.0
# Usage         : import config | from config import <clase>
# Notes         : Se han estructurado en clases las distintas configuraciones
#                 GPIOS contiene ternas de datos en formato lista:
#                 el primer elemento será el número (BCM) de puerto GPIO a manipular,
#                 el segundo, el modo (True para salida, False para entrada)
#                 y el tercero, la activación si es de salida (True si es activo a alto nivel o False si es a bajo nivel) o el estado si es de entrada (True si está bajado y False subido) 
#                 PAUSA (o PAUSAS, en el caso de reiniciar_router_config) contiene el/los tiempo(s) que el bucle estará parado
#                 senyales (señales) contiene el tipo de señal y la función a la que ésta se asociará
#                 
#                 A título ilustrativo, a se ofrece una configuración por defecto (la mía, para ser exactos)


class cpu_config:
    GPIOS           = [(26, True,  True ),
                       (19, True,  True ),
                       (13, True,  True ),
                       ( 6, True,  True ),
                       ( 5, True,  True ),
                      ]

    PAUSA           = 10

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }


class domotica_cliente_config:
    puerto          = 4710                                                      # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
                                                                                # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85


class domotica_servidor_config(domotica_cliente_config):
    GPIOS           = [(17, False, False),
                       (27, True,  False),
                       (23, False, False),
                       (24, True,  False),
                      ]

    PAUSA           = 0.25

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class internet_config:
    HOSTS           = ['google.es',
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


class reiniciar_router_config:
    GPIOS           = [( 4, True,  False),
                      ]

    PAUSA           = 15

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class temperaturas_config:
    GPIOS           = [(21, True,  True ),
                       (20, True,  True ),
                       (16, True,  True ),
                       (12, True,  True ),
                      ]

    TEMPERATURAS    = [40, 45, 50]

    PAUSA           = 60

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }
