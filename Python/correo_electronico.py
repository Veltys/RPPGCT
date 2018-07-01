#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : correo_electronico.py
# Description   : Sistema de envío de correos electrónicos
# Author        : Veltys
# Date          : 01-07-2018
# Version       : 1.0.0
# Usage         : from correo_electronico import mandar_correo
# Notes         :


DEBUG           = False
DEBUG_REMOTO    = False


import errno                                                                                # Códigos de error
import ssl                                                                                  # Seguridad
import sys                                                                                  # Funcionalidades varias del sistema

if DEBUG_REMOTO:
    import pydevd                                                                           # Depuración remota

try:
    from config import correo_electronico_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)

from email.mime.text import MIMEText                                                        # Codificación MIME
from smtplib import SMTP                                                                    # Envío de e-mails vía SMTP


def mandar_correo(de, para, asunto, correo):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    mensaje             = MIMEText(correo)
    mensaje['Subject']  = asunto
    mensaje['From']     = de
    mensaje['To']       = para

    s = SMTP(host = config.SERVIDOR)
    s.starttls(context = ssl.create_default_context())
    s.login(config.USUARIO, config.CONTRASENYA)
    s.send_message(mensaje)                                                                 # TODO: Probar los distintos fallos
    s.quit()

    return True


