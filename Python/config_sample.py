#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : config.py
# Description   : Módulo configurador para ser importado en el resto de módulos o sistemas que lo necesiten
# Author        : Veltys
# Date          : 29-11-2017
# Version       : 1.5.0
# Usage         : import config | from config import <clase>
# Notes         : A título ilustrativo, a se ofrece una configuración por defecto (la mía, para ser exactos)


class config_global:
    # Configuración común

    IP_DEP_REMOTA   = '0.0.0.0'                                                 # IP del servidor de depuración


class cpu_config(config_global):
    # Configuración del sistema de CPU

    GPIOS           = [(26, True,  True , 'Verde'                   ),          # GPIOS contiene ternas de datos en formato lista:
                       (19, True,  True , 'Amarillo'                ),          # el primer elemento será el número (BCM) de puerto GPIO a manipular,
                       (13, True,  True , 'Naranja'                 ),          # el segundo, el modo (True para salida, False para entrada)
                       ( 6, True,  True , 'Rojo'                    ),          # el tercero, la activación si es de salida (True si es activo a alto nivel o False si es a bajo nivel) o el estado si es de entrada (True si está bajado y False subido)
                       ( 5, True,  True , 'Alarma'                  ),          # y el cuarto, una muy breve descripción de su función
                      ]

    PAUSA           = 10                                                        # PAUSA contiene el tiempo que el bucle estará parado

    senyales        = {'SIGTERM': 'sig_cerrar',                                 # senyales (señales) contiene el tipo de señal y la función a la que ésta se asociará
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }


class domotica_cliente_config(config_global):
    puerto          = 4710                                                      # El puerto 4710 ha sido escogido arbitrariamente por estar libre, según la IANA:
                                                                                # https://www.iana.org/assignments/service-names-port-numbers/service-names-port-numbers.xhtml?&page=85


class domotica_servidor_config(domotica_cliente_config):
    GPIOS           = [(22, False, False, 'Botón, reinicio router'  ),          # En este caso, los puertos GPIO serán dados por pares, siendo el primer elemento el que hará de pulsador y el segundo sobre el que se operará
                       ( 4, True,  False, 'Relé reinicio router'    ),

                       (17, False, False, 'Botón (vacío)'           ),
                       (27, True,  False, 'Relé (vacío)'            ),

                       (23, False, False, 'Botón (vacío)'           ),
                       (24, True,  False, 'Relé (vacío)'            ),
                      ]

    PAUSA           = 0.20

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }


class internet_config(config_global):
    HOSTS           = ['google.es',                                             # HOSTS contiene los servidores a los cuales se les hará ping para comprobar si hay internet
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

    GPIO            = domotica_servidor_config.GPIOS[1]

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                      }

    servidor        = 'localhost'


class temperaturas_config(config_global):
    COLORES         = [(0.0, 0.0, 1.0, 0.0),                                    # COLORES contiene una matriz de 4 x 4 que, por columnas, representa cada led y, por filas, la etapa de temperatura
                       (0.0, 1.0, 0.0, 0.0),
                       (1.0, 0.6, 0.0, 0.0),
                       (1.0, 0.0, 0.0, 1.0),
                      ]

    FRECUENCIA      = 60                                                        # FRECUENCIA contiene la frecuencia (en herzios) de refresco de los leds

    GPIOS           = [(16, True,  True , 'Rojo'                    ),
                       (20, True,  True , 'Verde'                   ),
                       (21, True,  True , 'Azul'                    ),
                       (12, True,  True , 'Alarma'                  ),
                      ]

    TEMPERATURAS    = [40, 45, 50]                                              # TEMPERATURAS contiene las temperaturas de activación de cada etapa

    PAUSA           = 60

    senyales        = {'SIGTERM': 'sig_cerrar',
                       'SIGUSR1': 'sig_test',
                       'SIGUSR2': 'sig_apagado',
                      }
