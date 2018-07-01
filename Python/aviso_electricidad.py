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

try:
    from config import aviso_electricidad_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from correo_electronico import mandar_correo                                                # Envío de correos electrónicos


def main(argv):
    mandar_correo(config.DE, config.PARA, config.ASUNTO, config.CORREO)


if __name__ == '__main__':
    main(sys.argv)
