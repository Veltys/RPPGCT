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

from email.mime.text import MIMEText                                                        # Codificación MIME
from smtplib import SMTP, SMTPAuthenticationError                                           # Envío de e-mails vía SMTP y excepciones del envío
from socket import gaierror                                                                 # Excepciones del socket

try:
    from config import correo_electronico_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def mandar_correo(de, para, asunto, correo):
    if DEBUG_REMOTO:
        pydevd.settrace(config.IP_DEP_REMOTA)

    mensaje             = MIMEText(correo)
    mensaje['Subject']  = asunto
    mensaje['From']     = de
    mensaje['To']       = para

    try:
        s = SMTP(host = config.SERVIDOR)
        s.starttls(context = ssl.create_default_context())
        s.login(config.USUARIO, config.CONTRASENYA)

    except ConnectionRefusedError:
        res = False

    except gaierror:
        res = False

    except SMTPAuthenticationError:
        res = False

    else:
        s.send_message(mensaje)

        res = True

    finally:
        try:
            if s:
                s.quit()

        except UnboundLocalError:
            pass

    return res

