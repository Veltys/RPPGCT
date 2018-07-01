#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : aviso_electricidad.py
# Description   : Sistema de aviso en caso de corte de electricidad
# Author        : Veltys
# Date          : 01-07-2018
# Version       : 1.1.0
# Usage         : python3 aviso_electricidad.py
# Notes         :


import errno                                                                                # Códigos de error
import ssl                                                                                  # Seguridad
import sys                                                                                  # Funcionalidades varias del sistema

from time import sleep                                                                      # Para hacer pausas

try:
    from config import aviso_electricidad_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from correo_electronico import mandar_correo                                                # Envío de correos electrónicos


def main(argv):
    sleep(config.PAUSA * 6)                                                                 # Pausa inicial para esperar a que se levante la red

    for reintentos in range(config.REINTENTOS):
        if mandar_correo(config.DE, config.PARA, config.ASUNTO, config.CORREO):
            print('El correo ha podido ser enviado')

            enviado = True

            break

        else:
            print('El correo no ha podido ser enviado... reintentando ', reintentos, '/', config.REINTENTOS, 'veces', sep = '')

            enviado = False

            sleep(config.PAUSA)

    if enviado == False:
        print('Imposible reenviar el correo despues de', config.REINTENTOS, 'intentos')


if __name__ == '__main__':
    main(sys.argv)
