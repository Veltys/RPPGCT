#!/bin/bash

# Title         : desinstalador.sh
# Description   : Desinstala los scripts y los elimina la configuración para iniciarse automáticamente
# Author        : Veltys
# Date          : 29-06-2017
# Version       : 1.0.1
# Usage         : sudo bash desinstalador.sh
# Notes         : Es necesario ser superusuario para su correcto funcionamiento


if [ "$UID" -ne '0' ]; then
  echo 'Este script debe ser lanzado con permisos de root. ¿Quizá anteponiéndole la orden sudo?'
else
  /etc/init.d/temperaturas stop
  rm /usr/local/bin/pid.py
  rm /usr/local/bin/temperaturas.py
  rm /etc/init.d/temperaturas
  update-rc.d -f temperaturas remove

  /etc/init.d/cpu stop
  rm /usr/local/bin/cpu.py
  rm /etc/init.d/cpu
  update-rc.d -f cpu remove

  /etc/init.d/reiniciar_router stop
  rm /usr/local/bin/internet.py
  rm /usr/local/bin/reiniciar_router.py
  rm /etc/init.d/reiniciar_router
  update-rc.d -f reiniciar_router remove
fi




