#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : aviso_electricidad.py
# Description   : Sistema de aviso en caso de corte de electricidad
# Author        : Veltys
# Date          : 24-05-2018
# Version       : 1.0.0
# Usage         : python3 aviso_electricidad.py
# Notes         :


DEBUG           = False
DEBUG_REMOTO    = False


import errno                                                                                # Códigos de error
import ssl                                                                                  # Seguridad
import sys                                                                                  # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                           # Depuración remota

try:
    from config import aviso_electricidad_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from email.mime.text import MIMEText                                                        # Codificación MIME
from smtplib import SMTP                                                                    # Envío de e-mails vía SMTP


def main(argv):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    mensaje             = MIMEText(config.CORREO)
    mensaje['Subject']  = config.ASUNTO
    mensaje['From']     = config.DE
    mensaje['To']       = config.PARA

    s = SMTP(host = config.SERVIDOR)
    s.starttls(context = ssl.create_default_context())
    s.login(config.USUARIO, config.CONTRASENYA)
    s.send_message(mensaje)
    s.quit()


if __name__ == '__main__':
    main(sys.argv)
