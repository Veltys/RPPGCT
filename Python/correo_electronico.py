#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Title         : correo_electronico.py
# Description   : Sistema de envío de correos electrónicos
# Author        : Veltys
# Date          : 01-07-2018
# Version       : 1.0.1
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

if DEBUG_REMOTO:
    from pydevd_file_utils import setup_client_server_paths                                 # Configuración de las rutas Eclipse ➡

try:
    from config import correo_electronico_config as config                                  # Configuración

except ImportError:
    print('Error: Archivo de configuración no encontrado', file = sys.stderr)
    sys.exit(errno.ENOENT)


def mandar_correo(de, para, asunto, correo):
    if DEBUG_REMOTO:
        setup_client_server_paths(config.PYDEV_REMOTE_PATHS)

        pydevd.settrace(config.IP_DEP_REMOTA)

    mensaje             = MIMEText(correo)                                                  # Creación de un mensaje de correo en formato MIME
    mensaje['Subject']  = asunto
    mensaje['From']     = de
    mensaje['To']       = para

    try:                                                                                    # Bloque try
        s = SMTP(host = config.SERVIDOR)                                                    #     Conexión al servidor SMTP
        s.starttls(context = ssl.create_default_context())                                  #     Contexto SSL de seguridad
        s.login(config.USUARIO, config.CONTRASENYA)                                         #     Inicio de sesión

    except ConnectionRefusedError:                                                          # Rechazo de conexión por parte del servidor
        res = False

    except gaierror:                                                                        # Fallo de conectividad a Internet
        res = False

    except SMTPAuthenticationError:                                                         # Fallo de autenticación contra el servidor
        res = False

    else:                                                                                   # Si no hay excepciones
        s.send_message(mensaje)                                                             #     Envío del mensaje

        res = True

    finally:
        try:                                                                                # Bloque try
            if s:                                                                           #     Si el objeto existe y es válido
                s.quit()                                                                    #         Cierre de la sesión SMTP

        except UnboundLocalError:                                                           # Si el objeto no existe
            pass                                                                            #     No es necesaria ninguna operación adicional

    return res

