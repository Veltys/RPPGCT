#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : aviso_electricidad.py
# Description   : Sistema de aviso en caso de corte de electricidad
# Author        : Veltys
# Date          : 2021-04-30
# Version       : 1.1.3
# Usage         : python3 aviso_electricidad.py
# Notes         :


import errno                                                                                                                        # Códigos de error
import sys                                                                                                                          # Funcionalidades varias del sistema

from time import sleep                                                                                                              # Para hacer pausas

from correo_electronico import mandar_correo                                                                                        # Envío de correos electrónicos

try:
    from config import aviso_electricidad_config as config                                                                          # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def main(argv):
    sleep(config.PAUSA * 6)                                                                                                         # Pausa inicial para esperar a que se levante la red

    for reintentos in range(config.REINTENTOS):
        if mandar_correo(config.DE, config.PARA, config.ASUNTO, config.CORREO):                                                     # Si se ha podido mandar el correo
            print('El correo ha podido ser enviado')                                                                                #     Se informa de ello

            enviado = True                                                                                                          #     Bandera de estado

            break                                                                                                                   #     Se sale del bucle

        else:                                                                                                                       # Si no
            print('El correo no ha podido ser enviado... reintentando ', reintentos, '/', config.REINTENTOS, 'veces', sep = '')     #     Se informa de ello

            enviado = False                                                                                                         #     Bandera de estado

            sleep(config.PAUSA)                                                                                                     #     Pausa para reintentar

    if not(enviado):                                                                                                                # En caso de que haya sido imposible
        print('Imposible reenviar el correo despues de', config.REINTENTOS, 'intentos')                                             #    Se informa de ello


if __name__ == '__main__':
    main(sys.argv)
